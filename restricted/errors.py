"""
Errors library
"""
class UserExistsError(Exception):
    """
    User already exists and can't be created
    """
    pass


class PremissionError(Exception):
    """
    The process does not have the premissions to manage users and groups
    """

__all__ = ['UserExistsError', 'PremissionError']
