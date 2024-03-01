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


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    """Main dashboard of the website.
    It is the first page that the user sees when they visit the website.
    It displays the main features of the website and allows the user to navigate to different pages.
    """

    cur = mysql.connection.cursor()  # Create a cursor
    # cur.execute("INSERT INTO car_features VALUES('Swift Dzire', 2)")
    cur.execute("SELECT * FROM car_features")
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    # mysql.connection.commit()
    cur.close()  # Close the cursor

    alert = False  # True/False: Alert message is displayed or not
    global current_user_id
    current_user_id = 0
    session['user_id'] = 0
    return render_template("User/Dashboard.html",
                           alert=alert, logged_in=logged_in,
                           current_user_id=current_user_id,
                           name=name)


@app.route('/index')
def index():
    print(f"session['user_id']: {session['user_id']}")
    if session['user_id'] == 0:  # user is not logged in
        alert = False
        global name
        name = "yamete_kudasai"
        return redirect("/")

    car_data = get_car_data()
    return render_template("index.html", car_data=car_data)


def get_car_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM car_features")
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()

    return fetchdata


@app.route('/customerDashboard', methods=['GET', 'POST'])
def custLogin():
    global current_user_id
    bypass = request.args.get('bypass')

    if request.method == "POST":
        if 'sign_up' in request.form:
            print(f"request.form: {request.form}")
            alert = True
            action = "sign_up"
            customer_id = generate_customer_id(request.form['orangeForm-name'],
                                               request.form['orangeForm-age'], request.form['orangeForm-phone'])
            print(f"customer_id: {customer_id}")
            print(f"date.today(): {date.today()}")
            cur = mysql.connection.cursor()
            # str = ("INSERT INTO customer VALUES({customer_id}, %s, %s, %s, %s, %s, %s)", customer_id, request.form['orangeForm-name'], request.form['orangeForm-age'], request.form['orangeForm-phone'], request.form['orangeForm-email'], date.today(), request.form['orangeForm-pass'])
            str_customer = "INSERT INTO customer VALUES('{}','{}', {}, {}, '{}', '{}', '{}')".format(
                customer_id, request.form['orangeForm-name'], request.form['orangeForm-age'], request.form['orangeForm-phone'], request.form['orangeForm-email'], date.today(), request.form['orangeForm-pass'])
            print(f"str_customer: {str_customer}")
            cur.execute(str_customer)
            mysql.connection.commit()
            cur.close()

            current_user_id = customer_id
            print(f"current_user_id: {current_user_id}")
            session['user_id'] = current_user_id
            logged_in = True
        else:
            print(request.form)
            alert = True
            action = "login"
            cur = mysql.connection.cursor()
            str_check_customer = "SELECT customer_ID from customer where Password = '{}' and Email = '{}'".format(
                request.form['pass'], request.form['email'])
            temp = "SELECT * FROM customer"
            cur.execute(str_check_customer)
            customer_id = cur.fetchall()
            if (customer_id == ()):  # If the customer_id is empty, then the login is unsuccessful
                logged_in = False
                alert = False
                return render_template("User/Dashboard.html", alert=alert, name="unsuccessful", action=action, logged_in=logged_in)

            current_user_id = customer_id[0][0]
            session['user_id'] = current_user_id
            print(f"current_user_id: {current_user_id}")
            print(f"customer_id: {customer_id}")
            cur.close()
            logged_in = True
        # print(request.form['orangeForm-name'])
        # print(request.form['orangeForm-email'])
        # print(request.form['orangeForm-pass'])
    elif bypass == "0":
        alert = False
        action = " None"
        logged_in = True
    else:
        alert = False
    return render_template("User/Dashboard.html",
                           alert=alert, name="customer",
                           action=action, logged_in=logged_in)


@app.route('/employeeDashboard', methods=['GET', 'POST'])
def empLogin():

    if request.method == "POST":
        print(f"request.form: {request.form}")
        alert = True
        logged_in = True
        emp_ID = get_empid(request.form['email'], request.form['pass'])
        if emp_ID == None:
            logged_in = False
            alert = False
            return render_template("User/Dashboard.html",
                                   alert=alert, name="unsuccessful",
                                   action="login", logged_in=logged_in)
        session['user_id'] = emp_ID
    else:
        alert = False
    return render_template("User/Dashboard.html",
                           alert=alert, name="employee",
                           logged_in=logged_in)


def get_empid(email, password):
    s = f"SELECT emp_ID FROM employee WHERE Name = '{email}' and password = '{password}'"
    cur = mysql.connection.cursor()
    cur.execute(s)
    fetchdata = cur.fetchall()
    if fetchdata == ():
        return None
    print(f"fetchdata[0][0]: {fetchdata[0][0]}")  # employee ID
    cur.close()
    return fetchdata[0][0]


@app.route('/collections', methods=['GET', 'POST'])
def cars():
    return render_template("User/cars.html")


@app.route('/carDetails')
def carDetails():
    data = request.args.get('car_id')
    print(f"data: {data}")
    cur = mysql.connection.cursor()
    s = f"SELECT * FROM car_features WHERE car_ID = {data}"
    cur.execute(s)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()

    return render_template("User/car_details.html", fetchdata=fetchdata[0])


@app.route('/wishlist')
def wishlist():
    if session['user_id'] == 0:
        alert = False
        global name
        name = "yamete_kudasai"
        return redirect("/")
    print(f"session['user_id']: {session['user_id']}")
    car_id = request.args.get('car_id')
    action = request.args.get('action')
    print(f"car_id: {car_id}")
    print(f"action: {action}")
    if action == "0":
        cur = mysql.connection.cursor()
        s1 = f"DELETE FROM car_ownership WHERE owner_cust_id = '{session['user_id']}' and owned_car_id = {car_id}"
        cur.execute(s1)
        mysql.connection.commit()
        cur.close()
    elif car_id != None:
        assign_emp_id = get_emp_ids()
        cur = mysql.connection.cursor()
        s2 = f"INSERT INTO car_ownership VALUES('{session['user_id']}',{car_id},{assign_emp_id})"
        cur.execute(s2)
        mysql.connection.commit()
        cur.close()
    data = get_data()
    return render_template("User/wishlist.html", data=data)


def get_data():
    cur = mysql.connection.cursor()
    s = f"SELECT owned_car_id FROM car_ownership WHERE owner_cust_id = '{session['user_id']}'"
    cur.execute(s)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()
    lst = []  # list of car details
    for inner in fetchdata:
        for val in inner:
            cur = mysql.connection.cursor()
            s = f"SELECT car_name, image_link, price, car_ID FROM car_features WHERE car_ID = {val}"
            cur.execute(s)
            fetchdata = cur.fetchall()
            fetchdata = fetchdata[0]
            lst.append(fetchdata)
            print(f"fetchdata: {fetchdata}")
            cur.close()
    print(f"lst: {lst}")
    return lst


@app.route('/sales')
def sales():
    return render_template("User/sales.html")


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    temp_app_id = request.args.get('app_id')
    bypass = request.args.get('action')
    if bypass == "0":
        delete_entry(temp_app_id)
    if session['user_id'] == 0:
        alert = False
        global name
        name = "yamete_kudasai"
        return redirect("/")
    if request.method == "POST":
        datez = request.form['date']
        date = stemmed(datez)
        time = stem_time(datez)
        car_id = request.args.get('car_id')
        emp_id = get_emp_ids()
        app_id = gib_app_id_plz(session['user_id'], car_id, date)
        plz_push_all(app_id, date, time, emp_id, session['user_id'], car_id)
        print(date + " : " + time)
        print(f"car_id: {car_id}")
    print(f"session['user_id']: {session['user_id']}")
    lst = gen_list_to_pass(session['user_id'])
    return render_template("User/Appointments.html", list=lst)


def delete_entry(app_id):
    cur = mysql.connection.cursor()
    s = f"DELETE FROM appointment WHERE app_ID = '{app_id}'"
    cur.execute(s)
    mysql.connection.commit()
    cur.close()


def gen_list_to_pass(cust_id):
    s = f"SELECT Date, Time, Name, car_name, image_link, app_ID FROM appointment INNER JOIN car_features ON   appointment.Appointment_for_car_id = car_features.car_ID INNER JOIN employee ON appointment.handling_emp_id = employee.emp_ID WHERE appointment.booking_cust_id = '{cust_id}'"
    cur = mysql.connection.cursor()
    cur.execute(s)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()
    return fetchdata


def plz_push_all(app_id, date, time, emp_id, cust_id, car_id):
    cur = mysql.connection.cursor()
    s2 = f"INSERT INTO appointment VALUES('{app_id}','{date}','{time}',{emp_id},'{cust_id}',{car_id})"
    cur.execute(s2)
    mysql.connection.commit()
    cur.close()


def gib_app_id_plz(cust_id, car_id, date):
    s = cust_id[:4] + "_" + car_id + date[-2:]
    print(f"s: {s}")
    return s


def stemmed(date):
    s = ""
    for ch in date:
        if ch == 'T':
            break
        s += ch
    return s


def stem_time(date):
    s = ""
    flag = False
    for ch in date:
        if flag:
            s += ch
        if ch == 'T':
            flag = True
    return s


def get_emp_ids():
    cur = mysql.connection.cursor()
    s = "SELECT emp_ID FROM employee"
    cur.execute(s)
    fetchdata = cur.fetchall()
    cur.close()
    lst = []
    for ele in fetchdata:
        lst.append(ele[0])
    length = len(lst)
    chosen = random.randint(0, length-1)
    print(f"lst: {lst}")
    return lst[chosen]


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
