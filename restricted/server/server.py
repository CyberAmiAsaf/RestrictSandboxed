import json
import socket
import logging
from .user import User
from typing import List, Tuple, Mapping, Optional

Request = Tuple[str, Mapping]

class Server:
    def __init__(self, addr: str):
        self.addr = addr
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM | socket.SOCK_NONBLOCK)
        self.socket.bind(addr)
        self.sessions: List[User] = []
        self.requests: List[Request] = []
        self.buffer = ''

    def get_user(self, addr: str, token: str) -> Optional[User]:
        """
        Get the user represented by {token} in {addr} session
        """
        for user in self.sessions:
            if user.addr == addr and user.token == token:
                return user
        return None

    def handle(self, data: str, addr: str) -> Mapping:
        if self.buffer:
            data += self.buffer
            self.buffer = ''
        if not data.endswith('}'):
            *data, self.buffer = data.split('}{')
            data = '}{'.join(data)
            if data:
                if self.buffer:
                    self.buffer = '{' + self.buffer
                data += '}'
        if '}{' in data:
            data = f"[{data.replace('}{', '},{')}]"
        if not data:
            if not self.buffer:
                return {'status': False, 'return': 'No Data given'}
            else:
                return None
        try:
            request: Mapping = json.loads(data)
        except json.decoder.JSONDecodeError:
            print(data)
            return {'status': False, 'return': 'No JSON could be parsed'}
        print(addr, request)
        return {}

    def main(self):
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
            self.socket.sendto(bytes(response, 'ascii'), addr)
    