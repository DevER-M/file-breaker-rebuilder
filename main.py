def chunks(filepath:str):
    with open(filepath,'rb') as f:
        print(hash(f.peek(1024)))