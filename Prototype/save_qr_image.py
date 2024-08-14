import base64


def save_qr_image(base64_img, image_path):
    """Saves the base64 image to a file.

    Args:
        base64_img (str): The base64 image.
        image_path (str): The path to save the image.
    """

    # Convert the base64 image to bytes
    img_bytes = base64.b64decode(base64_img)

    # Save the image to a file
    with open(image_path, "wb") as img_file:
        img_file.write(img_bytes)
    print(f"✅ Saved the QR code to: {image_path}")
