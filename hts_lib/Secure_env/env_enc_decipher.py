import os
import subprocess
import re

class SecureEnvLoader:
    """
    A class to securely load API encrypted API keys from an encrypted .env file.
    """
    # Set the decryption password here
    password = "***REMOVED***"

    @staticmethod
    def openssl_decrypt(ciphertext: str) -> str | None:
        """
        Decrypts the encoded API key using OpenSSL and the provided password.
        Returns None if decryption fails.
        """
        process = subprocess.run(
            ["openssl", "enc", "-aes-256-cbc", "-d", "-a", "-salt", "-pass", f"pass:{SecureEnvLoader.password}"],
            input=ciphertext.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # If the process fails, return None
        if process.returncode != 0:
            return None

        # Attempt to decode the output, if it fails, return None
        try:
            return process.stdout.decode().strip()
        except UnicodeDecodeError:
            return None

    @staticmethod
    def load_env(filepath=os.path.join(os.path.dirname(__file__), ".env.enc")):
        """
        Loads API keys from an encrypted .env file and stores them in os.environ.
        If a key cannot be decrypted, it is skipped and a warning is printed.
        """
        if not os.path.exists(filepath):
            print(f"❌ Encrypted file '{filepath}' not found.")
            return
        
        # Read the encrypted file content
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Extract key-value pairs from the encrypted content
        encrypted_vars = dict(re.findall(r'(\w+)\s*=\s*"([^"]+)"', content, re.MULTILINE | re.DOTALL))

        # Iterate over each key-value pair, decrypting the value
        for key, encrypted_value in encrypted_vars.items():
            decrypted_value = SecureEnvLoader.openssl_decrypt(encrypted_value.strip())
            # If decryption was successful, set the environment variable
            if decrypted_value is not None:
                os.environ[key] = decrypted_value
                print(f"🔐 {key} loaded.")
            else:
                # If decryption failed, print a warning
                print(f"⚠️ Could not decrypt {key}. Make sure the decryption password is correct.")
