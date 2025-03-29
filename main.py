from hashlib import sha1


def chunks(filepath:str,chunksize:int):
    with open(filepath,'rb') as f:
        while f.read(1) != b'':
            print(sha1(f.read(chunksize)).hexdigest())
        
def tests(filepath):
    chunks(filepath,1024)

if __name__=='__main__':
    tests('randombin')