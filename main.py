from collections.abc import Callable, Buffer
from _hashlib import HASH


def chunks(filepath: str, chunksize: int, hasher: Callable[[Buffer], HASH]):
    with open(filepath, "rb") as f:
        while f.read(1) != b"":
            print(hasher(f.read(chunksize)).hexdigest())


def tests(filepath):
    from hashlib import sha1
    chunks(filepath, 1024,sha1)


if __name__ == "__main__":
    tests("randombin")
