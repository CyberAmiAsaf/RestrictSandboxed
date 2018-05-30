"""
Restricted User
"""
from restricted import User as _User
from restricted.utils import random_str


class User(_User):
    """
    A resticrtable user accessed via the server
    """
    def __init__(self, addr: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.addr = addr
        self.token = random_str(8)
