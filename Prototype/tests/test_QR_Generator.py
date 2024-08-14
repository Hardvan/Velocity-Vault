# Run as follows:
# cd to Prototype
# python -m unittest tests.test_QR_Generator

import unittest
import os
from QR_Generator import generate_employee_id, generate_customer_id, save_qr_code


class TestQRGenerator(unittest.TestCase):
    def test_generate_employee_id_format(self):
        name = "Alice"
        age = 28
        gender = "Female"
        salary = 60000
        employee_id = generate_employee_id(name, age, gender, salary)
        self.assertRegex(
            employee_id, r"alice_F_28_60k_\d{4}", "Employee ID format is incorrect")

    def test_generate_customer_id_format(self):
        name = "Bob"
        age = 30
        phone = "9876543210"
        customer_id = generate_customer_id(name, age, phone)
        self.assertRegex(
            customer_id, r"bob_3210_\d{4}", "Customer ID format is incorrect")

    def test_save_qr_code_employee(self):
        employee_id = "alice_F_28_60k_1234"
        folder = "test/QR_ID_Employee"
        image_path = save_qr_code(employee_id, user='E', folder=folder)
        self.assertTrue(os.path.exists(image_path),
                        "QR code image for employee was not saved correctly")
        self.assertEqual(
            image_path, f"{folder}/{employee_id}.png", "QR code image path is incorrect")
        os.remove(image_path)  # Clean up

    def test_save_qr_code_customer(self):
        customer_id = "bob_3210_1234"
        folder = "test/QR_ID_Customer"
        image_path = save_qr_code(customer_id, user='C', folder=folder)
        self.assertTrue(os.path.exists(image_path),
                        "QR code image for customer was not saved correctly")
        self.assertEqual(
            image_path, f"{folder}/{customer_id}.png", "QR code image path is incorrect")
        os.remove(image_path)  # Clean up


if __name__ == "__main__":
    unittest.main()
