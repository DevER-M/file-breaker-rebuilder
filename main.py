import pickle
import logging
from functools import partial
from os import path, makedirs
from traceback import format_exc

from collections.abc import Callable
from _hashlib import HASH


def tryex(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(format_exc())

    return wrapper


def chunk_hasher(filepath: str, chunksize: int, hasher: Callable[[bytes], HASH]):

    with open(filepath, "rb") as f:
        # partial creates function with default arg chunksize
        for chunk in iter(partial(f.read, chunksize), b""):
            # iter calls f.read(chunksize) until it returns b'' i.e the sentinel
            yield (hasher(chunk), chunk)


@tryex
def chunkify(filepath: str, chunksize: int, hasher: Callable[[bytes], HASH]):
    folder = f"{path.basename(filepath)}-chunks"
    hashes = [path.basename(filepath)]
    if not path.exists(folder):
        makedirs(folder)

    for chunk_hash, chunk in chunk_hasher(filepath, chunksize, hasher):
        with open(f"{folder}/{chunk_hash.hexdigest()}", "wb+") as f:
            f.write(chunk)
        hashes.append(chunk_hash.hexdigest())

    with open(f"{folder}/lookup", "wb+") as f:
        f.write(pickle.dumps(hashes))
    return hashes


@tryex
def rebuild(lookup: list[str]):
    if path.exists(lookup[0]):
        raise Exception("file already exists")
    with open(f"{lookup[0]}", "+ab") as f:
        for hash in lookup[1:]:
            with open(f"{lookup[0]}-chunks/{hash}", "rb") as data:
                f.write(data.read())


def tests(filepath):
    from hashlib import sha1

    # chunkify(filepath, 1024, sha1)
    with open("randombin-chunks/lookup", "rb") as f:
        li = pickle.load(f)
        rebuild(li)


@tryex
def sa(a):
    return a / 0


if __name__ == "__main__":
    from time import time

    sa(1)
    c = time()
    tests("randombin")
    print(time() - c)
