import logging
import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os


# Suppress the CUDA warning for easyocr
logging.getLogger('easyocr').setLevel(logging.ERROR)


def read_qr_code(image_path, show_image=False):
    """Reads the QR code from the given image and returns the decoded data.

    Args
    ----
    - `image_path`: path to the image containing the QR code.
    - `show_image`: whether to display the input image. Defaults to False.

    Returns
    -------
    - str: decoded data from the QR code.
    """

    # Display the input image
    if show_image:
        print("Press q to close the image")
        img = mpimg.imread(image_path)
        imgplot = plt.imshow(img)
        plt.title('Input QR Image')
        plt.show()

    # Read QR code data from the image
    qr_data = ""
    qr_img = cv2.imread(image_path)
    qr_results = decode(qr_img)
    if qr_results:
        qr_data = qr_results[0].data.decode('utf-8')

    return qr_data


if __name__ == "__main__":

    import time

    # Example usage
    def test_employee():

        print("Reading Employee QR code...\n")

        # Grab the first image from the folder test/QR_ID_Employee
        employee_folder = "./test/QR_ID_Employee"
        qr_image_path = os.listdir(employee_folder)[0]

        # Prepend the folder path to the image name
        qr_image_path = os.path.join(employee_folder, qr_image_path)

        # Read QR code data
        start_time = time.time()
        qr_code_data = read_qr_code(qr_image_path, show_image=True)
        elapsed_time = (time.time() - start_time)
        print(f"QR Code Data for Employee: {qr_code_data}")
        print(f"Time taken to read QR code: {elapsed_time:.2f}s")

    def test_customer():

        print("Reading Customer QR code...\n")

        # Grab the first image from the folder test/QR_ID_Customer
        customer_folder = "./test/QR_ID_Customer"
        qr_image_path = os.listdir(customer_folder)[0]

        # Prepend the folder path to the image name
        qr_image_path = os.path.join(customer_folder, qr_image_path)

        # Read QR code data
        start_time = time.time()
        qr_code_data = read_qr_code(qr_image_path, show_image=True)
        elapsed_time = (time.time() - start_time)
        print(f"QR Code Data for Customer: {qr_code_data}")
        print(f"Time taken to read QR code: {elapsed_time:.2f}s")

    test_employee()
    print("\n============================================\n")
    test_customer()

    # ! OCR is not reliable to read the user ID caption text in the QR code, so we will use the QR code data directly.
