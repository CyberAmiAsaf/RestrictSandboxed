"""
Set filesystem premissions
"""
from pathlib import Path
from typing import Optional, Dict
from ..server import Server


def main(server: Server, addr: str, token: str, path: str, mode: Optional[str] = None) -> Dict:
    user = server.get_user(addr, token)
    if user is None:
        return {'status': False, 'return': 'No user found'}
    kwargs = {}
    if mode:
        kwargs['mode'] = mode
    user.set_fs_file_premission(Path(path), **kwargs)
    