import logging
import easyocr
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


def read_employee_id(image_path):

    # Read Employee ID using OCR
    reader = easyocr.Reader(['en'])
    ocr_results = reader.readtext(image_path)
    employee_id = ""
    for result in ocr_results:
        if "Employee ID" in result[1]:
            # Remove the "Employee ID" text
            employee_id = result[1].replace("Employee ID", "").strip()
            # Remove the ":" text
            employee_id = employee_id.replace(":", "").strip()
            break

    return employee_id


if __name__ == "__main__":

    # Example usage
    qr_image_path = "./QR_ID/bob_M@30_50k_4023.png"

    # Display the input image
    img = mpimg.imread(qr_image_path)
    imgplot = plt.imshow(img)
    plt.title('Input Image')
    plt.show()

    # Read QR code data
    qr_code_data = read_qr_code(qr_image_path)
    print("QR Code Data:", qr_code_data)

    # Read Employee ID using OCR
    employee_id = read_employee_id(qr_image_path)
    print("Employee ID (OCR):", employee_id)

    # Check if the QR code data and OCR results match
    if qr_code_data == employee_id:
        print("✅ QR Code and OCR results match!")
    else:
        print("❌ QR Code and OCR results do not match!")
