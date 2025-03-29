from _hashlib import HASH
from functools import partial
from collections.abc import Callable, Buffer


def chunk_hasher(filepath: str, chunksize: int, hasher: Callable[[Buffer], HASH]):
    with open(filepath, 'rb') as f:
        # partial creates function with default arg chunksize
        for chunk in iter(partial(f.read, chunksize), b''):
            # iter calls f.read(chunksize) until it returns b'' i.e the sentinel
            yield hasher(chunk)


def tests(filepath):
    from hashlib import sha1

    print(chunk_hasher(filepath, 1024, sha1))


if __name__ == '__main__':
    tests('randombin')
