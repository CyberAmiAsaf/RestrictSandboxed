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
        self.sessions: List[User] = []
        self.requests: List[Request] = []

    def get_user(self, addr: str, token: str) -> Optional[User]:
        """
        Get the user represented by {token} in {addr} session
        """
        for user in self.sessions:
            if user.addr == addr and user.token == token:
                return user
        return None

    def handle(self, data: str, addr: str) -> Mapping:
        print(addr, data)

    def main(self):
        while True:
            try:
                data, addr = self.socket.recvfrom(1024)
            except BlockingIOError:
                continue
            if not addr:
                logging.info(f'Got data {data!r} from a client with no address')
                continue
            response = self.handle(data, addr) or ''
            response = json.dumps(response)
            self.socket.sendto(response, addr)
    