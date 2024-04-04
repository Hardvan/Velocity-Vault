"""
Functions present:
- generate_employee_id(name, age, gender, salary)
- generate_customer_id(name, age, phone)
- save_qr_code(user_id, user, folder)
"""

import random
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os


def generate_employee_id(name, age, gender, salary):

    # ID format: name_gender@age_salaryk_random4digits
    gender = 'M' if gender.lower() == 'male' else 'F'
    employee_id = f"{name.lower()}_{gender}_{age}_{salary/1000:.0f}k_{random.randint(1000, 9999)}"
    return employee_id


def generate_customer_id(name, age, phone):

    # ID format: name_age@phonelast4digits_random4digits
    customer_id = f"{name.lower()}_{phone[-4:]}_{random.randint(1000, 9999)}"
    return customer_id


def save_qr_code(user_id, user, folder='QR_ID'):
    """Generates a QR code with the given user ID and saves it to the specified folder.

    Args:
    - `user_id`: The user ID to be encoded in the QR code.
    - `user`: The type of user. Either 'E' for employee or 'C' for customer.
    - `folder`: The folder to save the QR code to. Defaults to 'QR_ID'.

    Returns:
    - str: The path to the saved QR code.

    Raises:
    - FileNotFoundError: If the logo for the user is not found.
    """

    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(user_id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Create image with caption
    img_with_caption = Image.new(
        'RGB', (qr_img.size[0], qr_img.size[1] + 50), color='white')
    img_with_caption.paste(qr_img, (0, 20))  # Move QR code down by 20 pixels

    # Add caption text
    draw = ImageDraw.Draw(img_with_caption)
    font_path = "./fonts/Roboto-Regular.ttf"
    font_size = 15
    font = ImageFont.truetype(font_path, font_size)
    caption = f"Employee ID: {user_id}" if user == 'E' else f"Customer ID: {user_id}"
    text_width = draw.textlength(caption, font)
    draw.text(((qr_img.size[0] - text_width) / 2, qr_img.size[1] + 10),
              caption, fill="black", font=font)

    # Add borders with spacing
    border_width = 3
    spacing = 10
    img_with_borders = ImageOps.expand(
        img_with_caption, border=border_width, fill='blue' if user == 'E' else 'green')
    img_with_borders = ImageOps.expand(
        img_with_borders, border=spacing, fill='white')

    # Offset the employee logo by 5 pixels from the top
    logo_path = "./static/images/emp_logo2.jpg" if user == 'E' else "./static/images/cust_logo.png"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50))  # Adjust the size as needed
        img_with_borders.paste(
            logo, ((img_with_borders.width - logo.width) // 2, spacing + 7))
    else:
        raise FileNotFoundError(f"Logo not found at {logo_path}")

    # Save image
    image_path = f"{folder}/{user_id}.png"
    img_with_borders.save(image_path)
    print(f"✅ Saved QR code to: {image_path}")

    return image_path


if __name__ == "__main__":

    def test_qr_generation():

        print("\nTesting QR code generation...\n")

        # Employee
        name = "Bob"
        age = 30
        gender = "Male"
        salary = 50000
        employee_id = generate_employee_id(name, age, gender, salary)
        print(f"Generated Employee ID: {employee_id}\n")
        save_qr_code(employee_id, user='E', folder='test/QR_ID_Employee')

        # Customer
        name = "Charlie"
        age = 25
        phone = "9876543210"
        customer_id = generate_customer_id(name, age, phone)
        print(f"Generated Customer ID: {customer_id}")
        save_qr_code(customer_id, user='C', folder='test/QR_ID_Customer')

    test_qr_generation()
