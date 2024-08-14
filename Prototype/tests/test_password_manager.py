# Run as follows:
# cd to Prototype
# python -m unittest tests.test_password_manager

import unittest
from password_manager import hash_password, check_password


class TestPasswordFunctions(unittest.TestCase):
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

    def test_check_password_correct(self):
        password = "test_password"
        hashed_password = hash_password(password)
        self.assertTrue(check_password(password, hashed_password),
                        "The password should match the hashed password")

    def test_check_password_incorrect(self):
        password = "test_password"
        wrong_password = "wrong_password"
        hashed_password = hash_password(password)
        self.assertFalse(check_password(wrong_password, hashed_password),
                         "The password should not match the hashed password")


if __name__ == "__main__":
    unittest.main()
