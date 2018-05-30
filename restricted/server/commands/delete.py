from typing import Dict
from ..user import User
from ..server import Server


def main(server: Server, addr: str, token: str) -> Dict:
    user = server.get_user(addr, token)
    if user is None:
        return {'status': False, 'return': 'No user found'}
    user.__del__()
    server.sessions.remove(user)
    return {'status': True}
    