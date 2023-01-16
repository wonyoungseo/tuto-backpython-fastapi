import bcrypt

if __name__ == "__main__":

    print(bcrypt.hashpw(b"secrete password", bcrypt.gensalt()))
    print(bcrypt.hashpw(b"secrete password", bcrypt.gensalt()).hex())