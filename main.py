from _hashlib import HASH
from functools import partial
from os import path, makedirs
from collections.abc import Callable, Buffer


def chunk_hasher(filepath: str, chunksize: int, hasher: Callable[[Buffer], HASH]):
    
    with open(filepath, 'rb') as f:
        # partial creates function with default arg chunksize
        for chunk in iter(partial(f.read, chunksize), b''):
            # iter calls f.read(chunksize) until it returns b'' i.e the sentinel
            yield (hasher(chunk), chunk)


def chunkify(filepath: str, chunksize: int, hasher: Callable[[Buffer], HASH]):
    folder=f'{path.basename(filepath)}-chunks'

    for chunk_hash, chunk in chunk_hasher(filepath, chunksize, hasher):
        if not path.exists(folder):
            makedirs(folder)
        with open(f'{folder}/{chunk_hash.hexdigest()}', 'wb+') as f:
            f.write(chunk)


def tests(filepath):
    from hashlib import sha1

    chunkify(filepath, 1024, sha1)


if __name__ == '__main__':
    from time import time

    c = time()
    tests('randombin')
    print(time() - c)
