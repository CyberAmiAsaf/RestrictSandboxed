import socket
import json
from typing import Optional

def create_socket(addr: str = '') -> socket.socket:
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(addr)
    return sock

def format(command: str, token: Optional[str] = None, **args) -> bytes:
    dct = {
        'command': command,
    }
    if token:
        dct['token'] = token
    if args:
        dct['args'] = args
    return json.dumps(dct).encode()