import os
from dotenv import load_dotenv
import random
import string

load_dotenv()


def get_env(key: str, fallback: str) -> str:
    """get environment variable value from .env

    Args:
        key (str): variable key
        fallback (str): fallback value if none

    Returns:
        str: value of environment variable
    """
    return os.getenv(key, fallback)


def generate_ref() -> str:
    """generate unique reference code"""
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return code.upper()
