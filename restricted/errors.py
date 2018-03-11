"""
Errors library
"""
class UserExistsError(Exception):
    """
    User already exists and can't be created
    """
    pass

__all__ = ['UserExistsError']
