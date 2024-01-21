import logging
import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Suppress the CUDA warning for easyocr
logging.getLogger('easyocr').setLevel(logging.ERROR)


def read_qr_code(image_path, show_image=False):

    # Display the input image
    if show_image:
        print("Press q to close the image")
        img = mpimg.imread(image_path)
        imgplot = plt.imshow(img)
        plt.title('Input Image')
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

        print("Employee QR code reading")
        qr_image_path = "./QR_ID_Employee/bob_M_30_50k_9151.png"

        # Read QR code data
        start_time = time.time()
        qr_code_data = read_qr_code(qr_image_path, show_image=True)
        elapsed_time = (time.time() - start_time)
        print("QR Code Data for Employee:", qr_code_data)
        print(f"Time taken to read QR code: {elapsed_time:.2f} s")

    def test_customer():

        print("Customer QR code reading")
        qr_image_path = "./QR_ID_Customer/charlie_3210_2757.png"

        # Read QR code data
        start_time = time.time()
        qr_code_data = read_qr_code(qr_image_path, show_image=True)
        elapsed_time = (time.time() - start_time)
        print("QR Code Data for Customer:", qr_code_data)
        print(f"Time taken to read QR code: {elapsed_time:.2f} s")

    test_employee()
    print("\n============================================\n")
    test_customer()

    # ! OCR is not reliable to read the user ID caption text in the QR code
