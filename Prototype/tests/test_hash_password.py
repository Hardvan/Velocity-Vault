# Run as follows:
# cd to Prototype
# python -m unittest tests.test_hash_password

import unittest
import bcrypt
from misc import hash_password  # Importing the function from misc.py


class TestHashPassword(unittest.TestCase):
    def test_hash_password_length(self):
        password = "test_password"
        hashed_password = hash_password(password)
        self.assertEqual(len(hashed_password), 60,
                         "Hashed password should be 60 characters long")

    def test_hash_password_type(self):
        password = "test_password"
        hashed_password = hash_password(password)
        self.assertIsInstance(hashed_password, str,
                              "Hashed password should be a string")

    def test_hash_password_consistency(self):
        password = "test_password"
        hashed_password1 = hash_password(password)
        hashed_password2 = hash_password(password)
        self.assertNotEqual(hashed_password1, hashed_password2,
                            "Hashed passwords should not be the same due to salting")

    def test_hash_password_verification(self):
        password = "test_password"
        hashed_password = hash_password(password)
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')),
                        "Original password should match the hashed password")


if __name__ == "__main__":
    unittest.main()
