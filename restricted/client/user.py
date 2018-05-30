import json
from pathlib import Path
from typing import Optional
from . import protocol


class User:
    def __init__(self, addr: str, user: Optional[str] = None, group: Optional[str] = None):
        args = {
            'user': user,
            'group': group
        }
        args = {key: val for key, val in args.items() if val}
        self.addr = addr
        self.socket = protocol.create_socket()
        self.socket.sendto(protocol.format('create', **args), addr)
        res = json.loads(self.socket.recvfrom(1024)[0].decode())
        if not res['status']:
            raise Exception(res['return'])
        self.user: str = res['return']['user']
        self.group: str = res['return']['group']
        self.token: str = res['return']['token']
        self.uid: int = res['return']['uid']

    def run_as(self, *command):
        """
        Wrap a command to run as the user
        """
        return ['su', self.user, '-c', ' '.join(command)]

    def delete(self):
        """
        Delete the user
        """
        self.socket.sendto(protocol.format('delete', token=self.token), self.addr)
        res = json.loads(self.socket.recvfrom(1024)[0].decode())
        if not res['status']:
            raise Exception(res['return'])

    def set_fs_file_premission(self, path: Path, mode: Optional[str] = None):
        """
        Set filesystem premissions
        """
        kwargs = {}
        if mode:
            kwargs['mode'] = mode
        self.socket.sendto(protocol.format('set_fs_file_premission', token=self.token, path=path, **kwargs), self.addr)
        res = json.loads(self.socket.recvfrom(1024)[0].decode())
        if not res['status']:
            raise Exception(res['return'])
