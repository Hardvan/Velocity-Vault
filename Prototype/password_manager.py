import bcrypt


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return str(hashed_password)[2:-1]


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


if __name__ == '__main__':

    password = 'abc123'
    print(f"Password: {password}")
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")
    print(f"Length of hashed password: {len(hashed_password)}")
    
    print(f"Is the password correct? {check_password(password, hashed_password)}")
