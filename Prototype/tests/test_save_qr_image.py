# Run as follows:
# cd to Prototype
# python -m unittest tests.test_save_qr_image


import unittest
import os
import base64
from save_qr_image import save_qr_image


class TestSaveQRImage(unittest.TestCase):

    def setUp(self):
        # Sample base64 image (this is just an example, a real base64 string should be used)
        self.sample_base64_img = base64.b64encode(
            b'sample image data').decode('utf-8')
        self.image_path = 'test_output/test_qr_image.png'

        # Create test_output directory if it doesn't exist
        os.makedirs('test_output', exist_ok=True)

    def test_save_qr_image(self):
        # Test saving the image
        save_qr_image(self.sample_base64_img, self.image_path)
        self.assertTrue(os.path.exists(self.image_path),
                        "The image file should exist after saving.")

    def test_save_multiple_qr_images(self):
        # Test saving multiple images
        for i in range(5):
            image_path = f'test_output/test_qr_image_{i}.png'
            save_qr_image(self.sample_base64_img, image_path)
            self.assertTrue(os.path.exists(image_path),
                            "The image file should exist after saving.")

    def test_save_qr_image_no_path(self):
        # Test saving the image without a path
        with self.assertRaises(TypeError):
            save_qr_image(self.sample_base64_img, None)

    def test_image_content(self):
        # Test the content of the saved image
        save_qr_image(self.sample_base64_img, self.image_path)
        with open(self.image_path, 'rb') as img_file:
            img_content = img_file.read()
        self.assertEqual(img_content, base64.b64decode(
            self.sample_base64_img), "The image content should match the decoded base64 data.")

    def tearDown(self):
        # Clean up: remove the test image file
        if os.path.exists(self.image_path):
            os.remove(self.image_path)

        # Clean up: remove the test images
        for i in range(5):
            image_path = f'test_output/test_qr_image_{i}.png'
            if os.path.exists(image_path):
                os.remove(image_path)

        # Remove the test_output directory
        if os.path.exists('test_output'):
            os.rmdir('test_output')


if __name__ == "__main__":
    unittest.main()
