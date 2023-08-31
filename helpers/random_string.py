## https://www.askpython.com/python/examples/generate-random-strings-in-python


import random


def random_string(length: int) -> str:

    random_str: str = ''

    for i in range(length):
        random_integer: int = random.randint(97, 122)
        random_str += (chr(random_integer))
    return random_str
