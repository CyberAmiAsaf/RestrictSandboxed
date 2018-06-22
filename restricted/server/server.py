"""
Server implementation
"""
import os
import json
import socket
import logging
from pathlib import Path
from types import ModuleType
from typing import List, Dict, Optional
from .user import User
from .commands import get_command


class Server:
    """
    Server
    """
    def __init__(self, addr: Path):
        self.addr = addr
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM | socket.SOCK_NONBLOCK)
        self.socket.bind(os.fspath(addr))
        addr.chmod(0o777)
        self.sessions: List[User] = []

    def get_user(self, addr: str, token: str) -> Optional[User]:
        """
        Get the user represented by {token} in {addr} session
        """
        for user in self.sessions:
            if user.addr == addr and user.token == token:
                return user
        return None

    def handle(self, data: str, addr: str) -> Dict:
        """
        Handle a message
        """
        if not data:
            return {'status': False, 'return': 'No Data was given'}
        try:
            request: Dict = json.loads(data)
        except json.JSONDecodeError:
            return {'status': False, 'return': 'No JSON could be parsed'}
        response: Dict = {}
        if 'command' not in request:
            response = {'status': False, 'return': 'No command was given'}
        else:
            command: str = request['command']
            module: Optional[ModuleType] = get_command(command)
            if not module:
                response = {'status': False, 'return': 'No such command was found'}
            else:
                kwargs = request.get('args', {})
                if 'token' in request:
                    kwargs['token'] = request['token']
                response = module.main(self, addr, **kwargs)
        ret = request.copy()
        ret.update(response)
        return ret

    def main(self):
        """
        Main loop
        """
        logging.info(f'Server started at {self.addr}')
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
            except BlockingIOError:
                continue
            if not addr:
                logging.info(f'Got data {data!r} from a client with no address')
                continue
            data = data.decode()
            response = self.handle(data, addr)
            if response is None:
                continue
            response = json.dumps(response)
            self.socket.sendto(response.encode(), addr)
    