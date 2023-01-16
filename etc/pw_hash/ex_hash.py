import hashlib

if __name__ == "__main__":

    m = hashlib.sha256()
    m.update(b"test password")
    h = m.hexdigest()
    print(h)