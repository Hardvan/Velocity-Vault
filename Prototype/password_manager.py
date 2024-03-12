import bcrypt


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password


def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == '__main__':
    
    password = 'abc123'
    print(f"Password: {password}")
    hashed_password = hash_password(password)
    print(f"Hashed password: {hashed_password}")
    print(f"Length of hashed password: {len(hashed_password)}")

    print(f"Check password: {check_password(password, hashed_password)}")
    print(f"Check password: {check_password('123abc', hashed_password)}")
