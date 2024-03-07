from flask import Flask, render_template, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from io import BytesIO
import base64
import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


# Testing Parameters
TEST_CONNECTION = True     # ? True/False: Test/Don't test the connection to MongoDB
# ? True/False: Test/Don't test the CRUD operations for the QR codes
TEST_CRUD_QR_CODE = True


# Define db and collection as placeholders
db = None
collection = None

# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))

# Select the database and collection
db = client['DBMS_db']
collection = db['qr_codes']

# Send a ping to confirm a successful connection
if TEST_CONNECTION:
    try:
        client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Add a sample document in the collection (don't add if already exists)
    name = 'John Doe'
    if collection.count_documents({'name': name}) == 0:
        collection.insert_one({'name': name})
        print("✅ Added a sample document in the collection.")

    # Retrieve the sample document added
    result = collection.find_one({'name': name})
    print(f"✅ Retrieved the sample document: {result}")

    # Delete the sample document added
    collection.delete_one({'name': name})
    print("✅ Deleted the sample document.")


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


# ? Routes

@app.route('/')
def index():
    return render_template("index.html")


# ? CRUD operations for the QR codes
# * Create
def add_qr_code(user_id, image_path, user):
    """Converts the image into base64 and adds a new QR code to the collection "qr_codes".

    Args:
        user_id (str): The user ID of the QR code.
        image_path (str): The path of the image.
        user (str): The type of user. Either 'E' for employee or 'C' for customer.
    """

    # Convert the image into base64
    with open(image_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode('utf-8')

    # Add the new QR code to the collection
    collection.insert_one({'user_id': user_id,
                           'image': base64_img,
                           'user': user})

    print(f"✅ Added a new QR code for {user} with user ID: {user_id}")


# * Read
def get_qr_code(user_id):
    """Retrieves the QR code from the collection "qr_codes".

    Args:
        user_id (str): The user ID of the QR code.

    Returns:
        dict: The retrieved QR code.
            Structure: {'user_id': str, 'image': str, 'user': str}
    """

    # Retrieve the QR code from the collection
    qr_code = collection.find_one({'user_id': user_id})
    print(f"✅ Retrieved the QR code for user ID: {user_id}")
    return qr_code


# * Update
def update_qr_code(user_id, image_path):
    """Converts the image into base64 and updates the QR code in the collection "qr_codes".

    Args:
        user_id (str): The user ID of the QR code.
        image_path (str): The path of the image.
    """

    # Convert the image into base64
    with open(image_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode('utf-8')

    # Update the QR code in the collection
    collection.update_one({'user_id': user_id},
                          {'$set': {'image': base64_img}})
    print(f"✅ Updated the QR code for user ID: {user_id}")


# * Delete
def delete_qr_code(user_id):
    """Deletes the QR code from the collection "qr_codes".

    Args:
        user_id (str): The user ID of the QR code.
    """

    # Delete the QR code from the collection
    collection.delete_one({'user_id': user_id})
    print(f"✅ Deleted the QR code for user ID: {user_id}")


if TEST_CRUD_QR_CODE:

    user_id = 'charlie_3210_2757'
    image_path = './QR_ID_Customer/charlie_3210_2757.png'

    # Create
    add_qr_code(user_id, image_path, 'C')

    # Read
    qr_code = get_qr_code(user_id)
    print("Retrieved data:\n")
    print(f"User ID: {qr_code['user_id']}")
    print(f"User: {qr_code['user']}")
    save_qr_image(qr_code['image'], user_id + "_retrieved.png")

    # Update
    update_qr_code(user_id, image_path)

    # Delete
    delete_qr_code(user_id)


if __name__ == "__main__":
    app.run(debug=True)