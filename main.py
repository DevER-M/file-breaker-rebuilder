from _hashlib import HASH
from functools import partial
from os import path, makedirs
import pickle
from collections.abc import Callable


def chunk_hasher(filepath: str, chunksize: int, hasher: Callable[[bytes], HASH]):

    with open(filepath, "rb") as f:
        # partial creates function with default arg chunksize
        for chunk in iter(partial(f.read, chunksize), b""):
            # iter calls f.read(chunksize) until it returns b'' i.e the sentinel
            yield (hasher(chunk), chunk)


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


def rebuild(lookup: list[str]):
    with (open(f"{lookup[0]}", "+ab")             as f,
         open(f"{lookup[0]}-chunks/{hash}", "rb") as data):
        for hash in lookup[1:]:
            f.write(data.read())


def tests(filepath):
    from hashlib import sha1

    # chunkify(filepath, 1024, sha1)
    with open("randombin-chunks/lookup", "rb") as f:
        li = pickle.load(f)
        rebuild(li)


if __name__ == "__main__":
    from time import time

    c = time()
    tests("randombin")
    print(time() - c)
