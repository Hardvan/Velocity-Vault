import logging
import cv2
from pyzbar.pyzbar import decode
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Suppress the CUDA warning for easyocr
logging.getLogger('easyocr').setLevel(logging.ERROR)


def read_qr_code(image_path):

    # Read QR code data from the image
    qr_data = ""
    qr_img = cv2.imread(image_path)
    qr_results = decode(qr_img)
    if qr_results:
        qr_data = qr_results[0].data.decode('utf-8')

    return qr_data


if __name__ == "__main__":

    # Example usage
    import time
    qr_image_path = "./QR_ID/bob_M@30_50k_1683.png"

    # Display the input image
    print("Press q to close the image")
    img = mpimg.imread(qr_image_path)
    imgplot = plt.imshow(img)
    plt.title('Input Image')
    plt.show()

    # Read QR code data
    start_time = time.time()
    qr_code_data = read_qr_code(qr_image_path)
    elapsed_time = (time.time() - start_time) * 1000
    print("QR Code Data:", qr_code_data)
    print(f"Time taken to read QR code: {elapsed_time:.2f} ms")

    # OCR is not reliable to read the employee ID caption text in the QR code
