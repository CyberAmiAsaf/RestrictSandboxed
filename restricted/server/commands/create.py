from typing import Optional, Dict
from restricted import UserExistsError
from ..user import User
from ..server import Server


def main(server: Server, addr: str, user: Optional[str] = None, group: Optional[str] = None) -> Dict:
    kwargs = {
        'user': user,
        'group': group
    }
    kwargs = {key: val for key, val in kwargs.items() if val}
    try:
        usr = User(addr, **kwargs)
    except UserExistsError:
        return {'status': False, 'return': 'User already exists'}
    server.sessions.append(usr)
    return {'status': True, 'return': {
        'user': usr.user,
        'group': usr.group,
        'uid': usr.uid,
        'token': usr.token
    }}
    