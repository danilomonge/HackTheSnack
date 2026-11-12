"""Shared pytest setup.

The app imports its modules as top-level packages (``backend.…``,
``frontend.…``) with ``hts_lib/`` on ``sys.path``, exactly like
``hts_lib/main.py`` does. Tests import them the same way so there is only one
copy of every module (and monkeypatching affects the code under test).
"""

import os
import sys

HTS_LIB_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "hts_lib"))
if HTS_LIB_DIR not in sys.path:
    sys.path.insert(0, HTS_LIB_DIR)

# Tests must never depend on real API keys or a running backend.
os.environ.pop("USDA_API_KEY", None)
os.environ.pop("AZURE_TRANSLATOR_KEY", None)
os.environ.pop("AZURE_TRANSLATOR_REGION", None)
os.environ["USER_MANAGEMENT_BASE_URL"] = "http://api.test/user-management"
