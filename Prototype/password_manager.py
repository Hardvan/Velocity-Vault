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


def check_password(password, hashed_password):
    """Checks if the password is correct.

    Args
    ----
    - `password`: input password.
    - `hashed_password`: hashed password.

    Returns
    -------
    - bool: True if the password is correct, False otherwise.
    """

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


if __name__ == '__main__':

    def test_password():

        print("Testing password hashing and checking...")

        password = 'abc123'
        print(f"Input Password: {password}\n")

        hashed_password = hash_password(password)
        print(f"Hashed password: {hashed_password}")
        print(f"Length of hashed password: {len(hashed_password)}\n")

        print(f"Is the password correct?")
        check = check_password(password, hashed_password)
        if check:
            print("✅ True")
        else:
            print("❌ False")

    test_password()
