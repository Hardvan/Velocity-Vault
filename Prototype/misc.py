import bcrypt


def hash_password(password):
    """Hashes the password using bcrypt algorithm.

    Args
    ----
    - `password`: input password to be hashed.

    Returns
    -------
    - str: hashed password.
    """

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    print(str(hashed_password)[2:-1])
    return str(hashed_password)[2:-1]  # Removing b'' from the hashed password


if __name__ == '__main__':
    hash_password("an27")
