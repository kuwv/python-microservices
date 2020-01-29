import os
import sys

# Required to test web layout
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)
# import app  # noqa: E402,F401
import security  # noqa: E402,F401
