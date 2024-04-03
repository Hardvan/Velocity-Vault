import base64

# ? CRUD operations for the QR codes


# * Create
def add_qr_code(user_id, image_path, user, mongo_collection):
    """Converts the image into base64 and adds a new QR code to the collection "qr_codes".

    Args
    ----
    - `user_id`: The user ID of the QR code.
    - `image_path`: The path of the image.
    - `user`: The type of user. Either 'E' for employee or 'C' for customer.
    - `mongo_collection`: The collection "qr_codes" in the MongoDB database.
    """

    # Convert the image into base64
    with open(image_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode('utf-8')

    # Add the new QR code to the collection
    mongo_collection.insert_one({'user_id': user_id,
                                 'image': base64_img,
                                 'user': user})

    print(f"✅ Added a new QR code for {user} with user ID: {user_id}")


# * Read
def get_qr_code(user_id, mongo_collection):
    """Retrieves the QR code from the collection "qr_codes".

    Args
    ----
    - `user_id`: The user ID of the QR code.
    - `mongo_collection`: The collection "qr_codes" in the MongoDB database.

    Returns
    -------
    - dict: The retrieved QR code.
        - Structure: {'user_id': str, 'image': str, 'user': str}
    """

    # Retrieve the QR code from the collection
    qr_code = mongo_collection.find_one({'user_id': user_id})
    print(f"✅ Retrieved the QR code for user ID: {user_id}")
    return qr_code


# * Update
def update_qr_code(user_id, image_path, mongo_collection):
    """Converts the image into base64 and updates the QR code in the collection "qr_codes".

    Args
    ----
    - `user_id`: The user ID of the QR code.
    - `image_path`: The path of the image.
    - `mongo_collection`: The collection "qr_codes" in the MongoDB database.
    """

    # Convert the image into base64
    with open(image_path, "rb") as img_file:
        base64_img = base64.b64encode(img_file.read()).decode('utf-8')

    # Update the QR code in the collection
    mongo_collection.update_one({'user_id': user_id},
                                {'$set': {'image': base64_img}})
    print(f"✅ Updated the QR code for user ID: {user_id}")


# * Delete
def delete_qr_code(user_id, mongo_collection):
    """Deletes the QR code from the collection "qr_codes".

    Args
    ----
    - `user_id`: The user ID of the QR code.
    - `mongo_collection`: The collection "qr_codes" in the MongoDB database.
    """

    # Delete the QR code from the collection
    mongo_collection.delete_one({'user_id': user_id})
    print(f"✅ Deleted the QR code for user ID: {user_id}")
