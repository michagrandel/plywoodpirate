# <> with ❤️ by Micha Grandel - hello@michagrandel.eu

""" Convert values """

__all__ = [
    'to_string'
]

from pathlib import Path
from typing import Any


def to_string(value: Any) -> str:
    """
    Convert any value to a string. For paths, return a posix path.
    
    Args:
        value: value to convert to string
    
    Returns:
        str: converted value
    """
    if isinstance(value, Path):
        return value.as_posix()
    if type(value) is type(True):
        print(value)
        return "True" if value is True else "False"
    return str(value)
