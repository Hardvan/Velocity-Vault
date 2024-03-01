from flask import Flask, render_template, request, jsonify, redirect, session
from QR_OCR_Generator import generate_customer_id
from flask_mysqldb import MySQL
from datetime import date
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import base64

import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.secret_key = 'lololol898989'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'carshowroom'

logged_in = False  # ? True/False: User is logged in or not
current_user_type = "blank"  # ? "customer"/"employee": Type of the current user
customer_id = "none"  # ? "customer_id": ID of the current customer
name = "none"  # ? "name": Name of the current user

mysql = MySQL(app)


# Testing Parameters
TEST_CONNECTION = True  # ? True/False: Test/Don't test the connection to MongoDB
# ? True/False: Test/Don't test the CRUD operations for the QR codes
TEST_CRUD_QR_CODE = True

# Define mongo_db and collection as placeholders
mongo_db = None
mongo_collection = None

# MongoDB connection
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))

# Select the database and collection
mongo_db = client['DBMS_db']
mongo_collection = mongo_db['qr_codes']

# Send a ping to confirm a successful connection
if TEST_CONNECTION:
    print("=== Testing MongoDB Connection ===")

    try:
        client.admin.command('ping')
        print("✅ Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # Add a sample document in the collection (don't add if already exists)
    name = 'John Doe'
    if mongo_collection.count_documents({'name': name}) == 0:
        mongo_collection.insert_one({'name': name})
        print("✅ Added a sample document in the collection.")

    # Retrieve the sample document added
    result = mongo_collection.find_one({'name': name})
    print(f"✅ Retrieved the sample document: {result}")

    # Delete the sample document added
    mongo_collection.delete_one({'name': name})
    print("✅ Deleted the sample document.")

    print("=== MongoDB Connection Test Completed ===")


# HTML File variables
dashboard_html = "User/dashboard.html"


# ? Routes

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    """Main dashboard of the website.
    It is the first page that the user sees when they visit the website.
    It displays the main features of the website and allows the user to navigate to different pages.
    """

    alert = False  # True/False: Alert message is displayed or not
    global current_user_id
    current_user_id = 0
    session['user_id'] = 0
    return render_template(dashboard_html,
                           alert=alert, logged_in=logged_in,
                           current_user_id=current_user_id,
                           name=name)


@app.route('/index')
def index():
    """Displays various cars available in the showroom.
    It allows the user to view the details of each car and add them to their wishlist.
    """

    print(f"session['user_id']: {session['user_id']}")
    if session['user_id'] == 0:  # user is not logged in
        global name
        name = "yamete_kudasai"  # dummy name
        return redirect("/")

    car_data = get_car_data()
    return render_template("index.html", car_data=car_data)


@app.route('/customerDashboard', methods=['GET', 'POST'])
def custLogin():
    """Customer login/signup page.
    After the user logs in or signs up, they are redirected to this page.
    """

    global current_user_id
    bypass = request.args.get('bypass')  # 0: Bypass the login/signup page

    if request.method == "POST":
        # * If the user is signing up
        if 'sign_up' in request.form:
            print(f"request.form: {request.form}")
            name = request.form['orangeForm-name']
            age = request.form['orangeForm-age']
            phone = request.form['orangeForm-phone']
            email = request.form['orangeForm-email']
            password = request.form['orangeForm-pass']

            alert = True
            action = "sign_up"
            customer_id = generate_customer_id(name, age, phone)
            print(f"customer_id: {customer_id}")
            print(f"date.today(): {date.today()}")

            # Insert the new customer into the "customer" table
            cur = mysql.connection.cursor()
            str_customer = f"INSERT INTO customer VALUES('{customer_id}','{name}', {age}, {phone}, '{email}', '{date.today()}', '{password}')"
            print(f"str_customer: {str_customer}")
            cur.execute(str_customer)
            mysql.connection.commit()
            cur.close()

            # TODO: Generate QR Code ID card of the customer

            current_user_id = customer_id
            print(f"current_user_id: {current_user_id}")
            session['user_id'] = current_user_id
            logged_in = True

        # If the user is logging in
        else:
            print(f"request.form: {request.form}")
            email = request.form['orangeForm-email']
            password = request.form['orangeForm-pass']

            # TODO: Add option of logging in with QR code

            alert = True
            action = "login"

            # Check if the customer exists in the "customer" table
            exists, customer_id = customerExists(email, password)
            if (not exists):
                logged_in = False
                alert = False
                return render_template(dashboard_html,
                                       alert=alert, name="unsuccessful",
                                       action=action, logged_in=logged_in)

            # Login successful
            logged_in = True
            current_user_id = customer_id[0][0]
            session['user_id'] = current_user_id
            print(f"current_user_id: {current_user_id}")
            print(f"customer_id: {customer_id}")

    elif bypass == "0":  # Bypass the login/signup page
        alert = False
        action = " None"
        logged_in = True
    else:
        alert = False

    return render_template(dashboard_html,
                           alert=alert, name="customer",
                           action=action, logged_in=logged_in)


@app.route('/employeeDashboard', methods=['GET', 'POST'])
def empLogin():

    if request.method == "POST":
        print(f"request.form: {request.form}")
        email = request.form['email']
        password = request.form['pass']

        alert = True
        logged_in = True

        emp_id = get_empid(email, password)
        if emp_id == None:  # Login unsuccessful
            logged_in = False
            alert = False
            return render_template(dashboard_html,
                                   alert=alert, name="unsuccessful",
                                   action="login", logged_in=logged_in)
        session['user_id'] = emp_id
    else:
        alert = False
    return render_template(dashboard_html,
                           alert=alert, name="employee",
                           logged_in=logged_in)


@app.route('/collections', methods=['GET', 'POST'])
def cars():
    return render_template("User/cars.html")


@app.route('/carDetails')
def carDetails():
    data = request.args.get('car_id')
    print(f"data: {data}")

    # Fetch the details of the selected car from "car_features" table
    cur = mysql.connection.cursor()
    s = f"SELECT * FROM car_features WHERE car_ID = {data}"
    cur.execute(s)
    fetchdata = cur.fetchall()
    cur.close()

    car_details = fetchdata[0]  # first car's details
    print(f"car_details: {car_details}")

    return render_template("User/car_details.html", fetchdata=car_details)


@app.route('/wishlist')
def wishlist():
    if session['user_id'] == 0:  # user is not logged in
        alert = False
        global name
        name = "yamete_kudasai"
        return redirect("/")

    print(f"session['user_id']: {session['user_id']}")
    car_id = request.args.get('car_id')
    action = request.args.get('action')
    print(f"car_id: {car_id}")
    print(f"action: {action}")

    if action == "0":  # delete the car from the wishlist
        cur = mysql.connection.cursor()
        s1 = f"DELETE FROM car_ownership WHERE owner_cust_id = '{session['user_id']}' and owned_car_id = {car_id}"
        cur.execute(s1)
        mysql.connection.commit()
        cur.close()
    elif car_id != None:  # add the car to the wishlist
        assign_emp_id = get_emp_ids()
        cur = mysql.connection.cursor()
        s2 = f"INSERT INTO car_ownership VALUES('{session['user_id']}',{car_id},{assign_emp_id})"
        cur.execute(s2)
        mysql.connection.commit()
        cur.close()

    data = get_data()
    return render_template("User/wishlist.html", data=data)


@app.route('/sales')
def sales():
    return render_template("User/sales.html")


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    temp_app_id = request.args.get('app_id')
    bypass = request.args.get('action')
    if bypass == "0":  # delete the appointment
        delete_entry(temp_app_id)
    if session['user_id'] == 0:  # user is not logged in
        global name
        name = "yamete_kudasai"
        return redirect("/")
    if request.method == "POST":
        # Create a new appointment
        input_date = request.form['date']
        date = stemmed(input_date)
        time = stem_time(input_date)

        car_id = request.args.get('car_id')
        emp_id = get_emp_ids()
        app_id = generate_app_id(session['user_id'], car_id, date)
        create_appointment(app_id, date, time, emp_id,
                           session['user_id'], car_id)

        print(f"{date} : {time}")
        print(f"car_id: {car_id}")

    print(f"session['user_id']: {session['user_id']}")
    appointments_list = get_appointments(session['user_id'])
    return render_template("User/Appointments.html", list=appointments_list)


def get_car_data():

    # Fetch the details of all the cars from the "car_features" table
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM car_features")
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()
    return fetchdata


def customerExists(email, password):
    """Checks if the customer exists in the "customer" table.

    Args:
        email (str): The customer's email.
        password (str): The customer's password.

    Returns:
        bool: True if the customer exists, False otherwise.
        str: The customer's ID if they exist, None otherwise.
    """
    cur = mysql.connection.cursor()
    str_check_customer = f"SELECT customer_ID from customer where Password = '{password}' and Email = '{email}'"
    cur.execute(str_check_customer)
    customer_id = cur.fetchall()
    cur.close()
    return bool(customer_id), customer_id


def get_empid(email, password):

    # Check if the employee exists in the "employee" table
    cur = mysql.connection.cursor()
    s = f"SELECT emp_ID FROM employee WHERE Name = '{email}' and password = '{password}'"
    cur.execute(s)
    fetchdata = cur.fetchall()
    cur.close()

    if fetchdata == ():  # no such employee
        return None

    # Return the employee ID
    emp_id = fetchdata[0][0]
    print(f"emp_id: {emp_id}")
    return emp_id


def get_data():

    # Fetch the details of all the cars in the wishlist from the "car_ownership" table
    cur = mysql.connection.cursor()
    s = f"SELECT owned_car_id FROM car_ownership WHERE owner_cust_id = '{session['user_id']}'"
    cur.execute(s)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()

    car_details = []  # list of car details
    for car in fetchdata:  # each car in the wishlist
        for car_id in car:  # each car's ID

            # Fetch the details of the car from the "car_features" table
            cur = mysql.connection.cursor()
            s = f"SELECT car_name, image_link, price, car_ID FROM car_features WHERE car_ID = {car_id}"
            cur.execute(s)
            fetchdata = cur.fetchall()
            fetchdata = fetchdata[0]
            car_details.append(fetchdata)
            print(f"fetchdata: {fetchdata}")
            cur.close()

    print(f"car_details: {car_details}")
    return car_details


def delete_entry(app_id):

    # Delete the appointment from the "appointment" table
    cur = mysql.connection.cursor()
    s = f"DELETE FROM appointment WHERE app_ID = '{app_id}'"
    cur.execute(s)
    mysql.connection.commit()
    cur.close()


def get_appointments(cust_id):

    # Generate the list of appointments to pass to the HTML file
    s = f"SELECT Date, Time, Name, car_name, image_link, app_ID FROM appointment INNER JOIN car_features ON   appointment.Appointment_for_car_id = car_features.car_ID INNER JOIN employee ON appointment.handling_emp_id = employee.emp_ID WHERE appointment.booking_cust_id = '{cust_id}'"
    cur = mysql.connection.cursor()
    cur.execute(s)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()
    return fetchdata


def create_appointment(app_id, date, time, emp_id, cust_id, car_id):

    # Insert the new appointment into the "appointment" table
    cur = mysql.connection.cursor()
    s2 = f"INSERT INTO appointment VALUES('{app_id}','{date}','{time}',{emp_id},'{cust_id}',{car_id})"
    cur.execute(s2)
    mysql.connection.commit()
    cur.close()


def generate_app_id(cust_id, car_id, date):

    # Generate the appointment ID
    app_id = cust_id[:4] + "_" + car_id + date[-2:]
    print(f"app_id: {app_id}")
    return app_id


def stemmed(date):
    # Extract the date from the datetime string
    s = ""
    for ch in date:
        if ch == 'T':
            break
        s += ch
    return s


def stem_time(date):
    # Extract the time from the datetime string
    s = ""
    flag = False
    for ch in date:
        if flag:
            s += ch
        if ch == 'T':
            flag = True
    return s


def get_emp_ids():

    # Fetch the employee IDs from the "employee" table
    cur = mysql.connection.cursor()
    s = "SELECT emp_ID FROM employee"
    cur.execute(s)
    fetchdata = cur.fetchall()
    cur.close()

    emp_ids = [e[0] for e in fetchdata]
    print(f"emp_ids: {emp_ids}")
    chosen = random.randint(0, len(emp_ids)-1)
    return emp_ids[chosen]


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
    mongo_collection.insert_one({'user_id': user_id,
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
    qr_code = mongo_collection.find_one({'user_id': user_id})
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
    mongo_collection.update_one({'user_id': user_id},
                                {'$set': {'image': base64_img}})
    print(f"✅ Updated the QR code for user ID: {user_id}")


# * Delete
def delete_qr_code(user_id):
    """Deletes the QR code from the collection "qr_codes".

    Args:
        user_id (str): The user ID of the QR code.
    """

    # Delete the QR code from the collection
    mongo_collection.delete_one({'user_id': user_id})
    print(f"✅ Deleted the QR code for user ID: {user_id}")


if TEST_CRUD_QR_CODE:

    print("=== Testing CRUD Operations for QR Codes ===")

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

    print("=== CRUD Operations for QR Codes Test Completed ===")


if __name__ == "__main__":
    # test_connection()
    app.run(debug=True)
