import random
import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
import os
from fpdf import FPDF


def generate_employee_id(name, age, gender, salary):
    # Generate id from attributes + 4 digit random number
    gender = 'M' if gender.lower() == 'male' else 'F'
    employee_id = f"{name.lower()}_{gender}@{age}_{salary/1000:.0f}k_{random.randint(1000, 9999)}"
    return employee_id


def save_qr_code(employee_id, folder='QR_ID'):

    # Create folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(employee_id)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="green", back_color="white")

    # Create image with caption
    img_with_caption = Image.new(
        'RGB', (qr_img.size[0], qr_img.size[1] + 50), color='white')
    img_with_caption.paste(qr_img, (0, 20))  # Move QR code down by 20 pixels

    # Add caption text
    draw = ImageDraw.Draw(img_with_caption)
    font_path = "./fonts/Roboto-Regular.ttf"
    font_size = 15
    font = ImageFont.truetype(font_path, font_size)
    caption = f"Employee ID: {employee_id}"
    text_width = draw.textlength(caption, font)
    draw.text(((qr_img.size[0] - text_width) / 2, qr_img.size[1] + 10),
              caption, fill="black", font=font)

    # Add borders with spacing
    border_width = 3
    spacing = 10
    img_with_borders = ImageOps.expand(
        img_with_caption, border=border_width, fill='blue')
    img_with_borders = ImageOps.expand(
        img_with_borders, border=spacing, fill='white')

    # Offset the employee logo by 5 pixels from the top
    logo_path = "./static/images/emp_logo2.jpg"
    if os.path.exists(logo_path):
        logo = Image.open(logo_path)
        logo = logo.resize((50, 50))  # Adjust the size as needed
        img_with_borders.paste(
            logo, ((img_with_borders.width - logo.width) // 2, spacing + 7))
    else:
        raise FileNotFoundError("Employee logo not found!")

    # Save image
    image_path = f"{folder}/{employee_id}.png"
    img_with_borders.save(image_path)
    print("✅ Saved QR code to:", image_path)


def save_ocr_pdf(employee_id, name, age, gender, salary):

    # Create OCR_PDF folder if it doesn't exist
    os.makedirs("OCR_PDF", exist_ok=True)

    # Create PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Times", size=12)

    # Set the heading of the PDF as Employee ID
    pdf.cell(200, 10, txt=employee_id, ln=True, align='C')

    # Add employee attributes & values
    attributes = ["Name", "Age", "Gender", "Salary"]
    values = [name, str(age), gender, f"${salary:,}"]

    for attribute, value in zip(attributes, values):
        pdf.cell(200, 10, txt=f"{attribute}: {value}", ln=True, align='L')

    # Save the PDF
    pdf_output_path = f"OCR_PDF/{employee_id}.pdf"
    pdf.output(pdf_output_path)
    print("✅ Saved OCR PDF to:", pdf_output_path)


if __name__ == "__main__":

    # Example usage
    name = "Bob"
    age = 30
    gender = "Male"
    salary = 50000

    employee_id = generate_employee_id(name, age, gender, salary)
    print("Generated Employee ID:", employee_id)

    save_qr_code(employee_id)
    save_ocr_pdf(employee_id, name, age, gender, salary)
