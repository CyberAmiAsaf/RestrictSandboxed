import os
import json
import pexpect
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
        try:
            self.socket.sendto(protocol.format('create', **args), addr)
        except FileNotFoundError:
            raise RuntimeError('Could not connect to server')
        res = json.loads(self.socket.recvfrom(1024)[0].decode())
        if not res['status']:
            raise Exception(res['return'])
        self.user: str = res['return']['user']
        self.group: str = res['return']['group']
        self.token: str = res['return']['token']
        self.uid: int = res['return']['uid']

    def run_as(self, *command: str) -> int:
        """
        Run a command as the user

        :return: return code
        """
        command = ['su', self.user, '-c', ' '.join(command)]
        ps = pexpect.spawn(command[0], command[1:])
        ps.expect('(?i)password: ')
        ps.waitnoecho()
        ps.sendline(self.token)
        ps.expect('\n')
        ps.interact()
        ps.expect(pexpect.EOF)
        ps.close()

        return ps.exitstatus

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
        self.socket.sendto(protocol.format('set_fs_file_premission', token=self.token, path=os.fspath(path), **kwargs), self.addr)
        res = json.loads(self.socket.recvfrom(1024)[0].decode())
        if not res['status']:
            raise Exception(res['return'])
