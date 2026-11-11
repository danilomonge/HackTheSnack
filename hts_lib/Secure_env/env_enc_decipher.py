"""Loads the USDA / DeepL API keys for desktop runs.

Keys are read, in this order:

1. Already-set environment variables ``USDA_API_KEY`` / ``DEEPL_API_KEY``
   (e.g. exported in your shell). Nothing else is needed then.
2. The encrypted file ``Secure_env/.env.enc``. Each value was encrypted with::

       echo -n "<key>" | openssl enc -aes-256-cbc -a -salt -pass pass:<password>

   and is decrypted with the password from the ``HTS_ENV_PASSWORD``
   environment variable. ``openssl`` must be installed.

The public web build never uses this module; it gets nutrition data from the HackTheSnackDB API.
"""

import os
import re
import shutil
import subprocess


class SecureEnvLoader:
    """Decrypts API keys from ``.env.enc`` into ``os.environ``."""

    #: Environment variable that holds the decryption password.
    PASSWORD_ENV_VAR = "HTS_ENV_PASSWORD"

    @staticmethod
    def openssl_decrypt(ciphertext: str, password: str) -> str | None:
        """
        Decrypts one base64 value with OpenSSL. Returns None on any failure.
        """
        if not shutil.which("openssl"):
            return None
        try:
            process = subprocess.run(
                ["openssl", "enc", "-aes-256-cbc", "-d", "-a", "-salt", "-pass", f"pass:{password}"],
                input=(ciphertext.strip() + "\n").encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError:
            return None
        if process.returncode != 0:
            return None
        try:
            return process.stdout.decode().strip() or None
        except UnicodeDecodeError:
            return None

    @staticmethod
    def load_env(filepath: str = os.path.join(os.path.dirname(__file__), ".env.enc")) -> None:
        """
        Sets every decryptable ``KEY="<ciphertext>"`` entry of ``filepath`` as an
        environment variable, unless that variable is already set. Silent when
        there is nothing to do (no file or no password).
        """
        password = os.environ.get(SecureEnvLoader.PASSWORD_ENV_VAR)
        if not password or not os.path.exists(filepath):
            return

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        encrypted_vars = dict(re.findall(r'(\w+)\s*=\s*"([^"]+)"', content, re.MULTILINE | re.DOTALL))
        for key, encrypted_value in encrypted_vars.items():
            if os.environ.get(key):
                continue
            decrypted_value = SecureEnvLoader.openssl_decrypt(encrypted_value, password)
            if decrypted_value is not None:
                os.environ[key] = decrypted_value
            else:
                print(f"⚠️ Could not decrypt {key}. Check {SecureEnvLoader.PASSWORD_ENV_VAR}.")
