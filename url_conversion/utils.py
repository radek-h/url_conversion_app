import random
import string


def generate_url_key(length: int = 5) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))
