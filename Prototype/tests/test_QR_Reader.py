# Run as follows:
# cd to Prototype
# python -m unittest tests.test_QR_Reader

import unittest
import os
import cv2
from QR_Reader import read_qr_code
import numpy as np


class TestQRReader(unittest.TestCase):

    def setUp(self):
        # Setup paths to test QR images
        self.employee_qr_path = "../test/QR_ID_Employee"
        self.customer_qr_path = "../test/QR_ID_Customer"

        # Check that test QR code images exist
        self.employee_qr_image = os.path.join(
            self.employee_qr_path, os.listdir(self.employee_qr_path)[0])
        self.customer_qr_image = os.path.join(
            self.customer_qr_path, os.listdir(self.customer_qr_path)[0])

    def test_read_qr_code_employee(self):
        qr_data = read_qr_code(self.employee_qr_image)
        self.assertTrue(qr_data.startswith(
            "bob"), "QR data for the employee should start with the name 'bob'")

    def test_read_qr_code_customer(self):
        qr_data = read_qr_code(self.customer_qr_image)
        self.assertTrue(qr_data.startswith(
            "charlie"), "QR data for the customer should start with the name 'charlie'")

    def test_read_qr_code_no_data(self):
        empty_image_path = "./test/empty_qr.png"
        # Create an empty image for testing
        empty_img = cv2.imwrite(
            empty_image_path, 255 * np.ones((100, 100, 3), dtype=np.uint8))
        qr_data = read_qr_code(empty_image_path)
        self.assertEqual(
            qr_data, "", "QR data should be empty if there is no QR code in the image")
        os.remove(empty_image_path)  # Clean up

    def test_read_qr_code_invalid_path(self):
        with self.assertRaises(TypeError, msg="cannot unpack non-iterable NoneType object"):
            read_qr_code("invalid_path.png")


if __name__ == "__main__":
    unittest.main()
