import random
import string


def random_str(n):
    """
    Generate a {n} length random string from uppercase characters and digits
    """
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
