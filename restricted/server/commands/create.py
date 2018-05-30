from typing import Optional, Dict
from restricted import UserExistsError
from ..user import User
from ..server import Server


def main(server: Server, addr: str, uname: Optional[str] = None, group: Optional[str] = None) -> Dict:
    kwargs = {
        'user': uname,
        'group': group
    }
    kwargs = {key: val for key, val in kwargs.items() if val}
    try:
        user = User(addr, **kwargs)
    except UserExistsError:
        return {'status': False, 'return': 'User already exists'}
    server.sessions.append(user)
    return {'status': True, 'return': {
        'user': user.user,
        'group': user.group,
        'uid': user.uid,
        'token': user.token
    }}
    