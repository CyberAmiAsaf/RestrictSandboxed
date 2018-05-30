"""
Commands mechanism for the server
"""
import os
import importlib
from pathlib import Path
from types import ModuleType
from typing import Generator, Optional


def list_commands() -> Generator[str, None, None]:
    """
    Generate a list of all available commands
    """
    for entry in os.scandir(Path(__file__).parent):
        entry: os.DirEntry = entry
        if entry.is_file() and entry.name.endswith('.py') and not entry.name.startswith('_'):
            yield entry.name[:-3]


def get_command(command: str) -> Optional[ModuleType]:
    """
    Get the module of the {command} command
    """
    if not command in list_commands():
        return None
    return importlib.import_module(f'.{command}', __package__)
