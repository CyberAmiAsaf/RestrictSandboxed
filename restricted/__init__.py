"""
Library
"""
import logging
from .consts import *
from .errors import *
from .lib import *

logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s')

del logging
