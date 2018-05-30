import socket
import json
from typing import Optional


def create_socket(addr: str = '') -> socket.socket:
    """
    Create a Bound UNIX DATAGRAM Socket
    """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
    sock.bind(addr)
    return sock


def format(command: str, token: Optional[str] = None, **args) -> bytes:
    """
    Format a message by the protocol
    """
    dct = {
        'command': command,
    }
    if token:
        dct['token'] = token
    if args:
        dct['args'] = args
    return json.dumps(dct).encode()
