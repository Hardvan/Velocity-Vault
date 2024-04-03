from flask import Flask, render_template, request, jsonify, redirect, session, url_for
from flask_mysqldb import MySQL
from datetime import date
import time
import stripe
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import base64
import stripe

# Custom modules
from QR_OCR_Generator import generate_customer_id, generate_employee_id, save_qr_code
from CRUD_QR import add_qr_code, get_qr_code, update_qr_code, delete_qr_code
from HuggingFace import sentiment_analysis, summarize_text


import os
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

# SQL Configuration
app.secret_key = 'lololol898989'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car_showroom'

# User variables
logged_in = False  # ? True/False: User is logged in or not
current_user_type = "blank"  # ? "customer"/"employee": Type of the current user
customer_id = "none"  # ? "customer_id": ID of the current customer
name = "none"  # ? "name": Name of the current user

mysql = MySQL(app)

stripe_keys = {
    "secret_key": "sk_test_51OqBUDSDxbyR6TDXKq1yk8FCTIRGukANTOgdCUyChhRf4YmoqubpGmDo0JSdxSkEMjxEklUIZECY61bRPzjlgFpD00yfhA9sr7",
    "publishable_key": "pk_test_51OqBUDSDxbyR6TDXyVusFbV7IChPwvs8PzdP6AXt65JSi9gObEyC66XB33oKuf4UvXSgaIk9gB8TqDmKQLrnlfFY00opHauWOd",
}

stripe.api_key = stripe_keys["secret_key"]


# Testing Parameters
TEST_CONNECTION = True  # ? Test/Don't test the connection to MongoDB
TEST_CRUD_QR_CODE = True  # ? Test/Don't test the CRUD operations for the QR codes

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


if TEST_CRUD_QR_CODE:

    print("=== Testing CRUD Operations for QR Codes ===")

    user_id = 'charlie_3210_2757'
    image_path = 'Prototype/QR_ID_Customer/charlie_3210_2757.png'

    # Create
    add_qr_code(user_id, image_path, 'C', mongo_collection)

    # Read
    qr_code = get_qr_code(user_id, mongo_collection)
    print("Retrieved data:\n")
    print(f"User ID: {qr_code['user_id']}")
    print(f"User: {qr_code['user']}")
    save_qr_image(qr_code['image'], user_id + "_retrieved.png")

    # Update
    update_qr_code(user_id, image_path, mongo_collection)

    # Delete
    delete_qr_code(user_id, mongo_collection)

    print("=== CRUD Operations for QR Codes Test Completed ===")


# HTML File variables
dashboard_html = "User/dashboard.html"


# SQL Functions
def read_query(query):
    """Executes a SELECT query on the database.
    This function greatly simplifies the process of executing a query
    by reducing the no. of lines of code required and improving readability.

    Args
    ----
    - query (str): The SQL query to execute.

    Returns
    -------
    - list: The result of the query
    """

    cur = mysql.connection.cursor()
    cur.execute(query)
    result = cur.fetchall()
    cur.close()
    return result


def write_query(query):
    """Executes a INSERT/DELETE/UPDATE query on the database.
    This function greatly simplifies the process of executing a query
    by reducing the no. of lines of code required and improving readability.

    Args
    ----
    - query (str): The SQL query to execute.
    """

    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    cur.close()


# ? Routes
# /: Main dashboard of the website
# /index: Displays various cars available in the showroom
# /customerDashboard: Customer login/signup page
# /employeeDashboard: Employee login page
# /collections: Displays the collection of cars
# /carDetails: Displays the details of a car
# /wishlist: Displays the wishlist of the user
# /charge: Charges the user for the car
# /sales: Displays the sales page
# /appointments: Displays the appointments page


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
        # * Signing up the user
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
            write_query(
                f"INSERT INTO customer VALUES('{customer_id}','{name}', {age}, {phone}, '{email}', '{date.today()}', '{password}')")

            # Create the QR code of the customer
            #image_path = save_qr_code(
            #    customer_id, user="C", folder="QR_ID_Customer")

            # Add the new QR code to the collection "qr_codes"
            #add_qr_code(customer_id, image_path, "C", mongo_collection)

            # #Save the customer ID in the session      

            current_user_id = customer_id
            print(f"current_user_id: {current_user_id}")
            session['user_id'] = current_user_id
            logged_in = True

        # * Logging in the user
        else:
            print(f"request.form: {request.form}")
            email = request.form['email']
            password = request.form['pass']

            alert = True
            action = "login"

            # Check if the customer exists in the "customer" table
            exists, customer_id = customerExists(email, password)
            if not exists:
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

    # Get QR code of the customer
    #qr_code = get_qr_code(current_user_id, mongo_collection)
    #qr_image = qr_code['image']
        # qr_image=qr_image

    return render_template(dashboard_html,
                           alert=alert, name="customer",
                           action=action, logged_in=logged_in,)


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
    fetchdata = read_query(f"SELECT * FROM car_features WHERE car_ID = {data}")

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
    mode = request.args.get('mode')
    print(f"car_id: {car_id}")
    print(f"action: {action}")

    if action == "1":  # buy the car from the wishlist
        sale_date = date.today()
        final_price = request.args.get('final_price')
        if mode:
            payment_method = "crypto"
        else:
            payment_method = "visa"
        sale_to_cust_id = session['user_id']
        sale_by_emp_id = get_emp_who_sold(session['user_id'], car_id)
        sale_involved_car_id = car_id
        sale_id = gen_sale_id(session['user_id'],
                              sale_involved_car_id, sale_by_emp_id)

        write_query(
            f"DELETE FROM car_ownership WHERE owner_cust_id = '{session['user_id']}' and owned_car_id = {car_id}")
        write_query(
            f"INSERT INTO sale VALUES('{sale_id}','{sale_date}',{final_price},'{payment_method}','{sale_to_cust_id}',{sale_by_emp_id},{sale_involved_car_id})")

    elif action == "0":  # delete the car from the wishlist
        write_query(
            f"DELETE FROM car_ownership WHERE owner_cust_id = '{session['user_id']}' and owned_car_id = {car_id}")
    elif car_id != None:  # add the car to the wishlist
        assign_emp_id = get_emp_ids()
        write_query(
            f"INSERT INTO car_ownership VALUES('{session['user_id']}',{car_id},{assign_emp_id})")

    data = get_wishlist_data()
    return render_template("User/wishlist.html", data=data, key=stripe_keys['publishable_key'])


def gen_sale_id(cust_id, car_id, emp_id):
    sale_id = f"{cust_id[:4]}_{car_id}_{emp_id}_{date.today()}"
    print(f"sale_id: {sale_id}")
    return sale_id


def get_emp_who_sold(cust_id, car_id):
    fetchdata = read_query(
        f"SELECT emp_ID FROM car_ownership where owner_cust_id = '{cust_id}' and owned_car_id = {car_id}")

    emp_id = fetchdata[0][0]
    return emp_id


@app.route('/charge', methods=['POST'])
def charge():
    # Amount in cents
    amount = 1000

    car_id = request.form['car_id']
    final_price = request.form['final_price']
    action = request.form['action']

    s = f"{session['user_id']}_{final_price}"

    customer = stripe.Customer.create(
        email="karan@gmail.com",
        source=request.form['stripeToken']
    )

    stripe.PaymentIntent.create(
        amount=1000,
        currency="inr"
    )

    return redirect(url_for('wishlist', car_id=car_id, action=action, final_price=final_price))


@app.route('/sales')
def sales():
    emp_id = session['user_id']
    data = get_sale_data(emp_id)
    return render_template("User/sales.html", data=data)


def get_sale_data(emp_id):
    fetchdata = read_query(
        f"SELECT car_name, Name, final_price, sale_date, payment_method, image_link FROM sale INNER JOIN customer ON sale_to_cust_id = customer_ID INNER JOIN car_features ON sale_involved_car_id = car_ID WHERE sale_by_emp_id = {emp_id}")

    return fetchdata

@app.route('/profile')
def profile():
    cust_data = customer_data()
    bought_data = get_bought_car_data()
    return render_template("User/profile_user.html", cust_data = cust_data, bought_data = bought_data)

@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    temp_app_id = request.args.get('app_id')
    bypass = request.args.get('action')

    if bypass == "0":  # delete the appointment
        delete_appointment(temp_app_id)

    if session['user_id'] == 0:  # user is not logged in
        global name
        name = "yamete_kudasai"
        return redirect("/")

    if request.method == "POST":  # Create a new appointment
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

@app.route('/emp_profile')
def emp_profile():
    emp_data = get_emp_data()
    sold_data = get_sold_data()
    incentive = calc_emp_incentive()
    return render_template('User/profile_employee.html', emp_data = emp_data, sold_data = sold_data, incentive = incentive)

@app.route('/enter_review', methods = ['GET', 'POST'])
def enter_review():
    if request.method == 'POST':
        des = request.form['des']
        rating = request.form['rating']
        print(des)
        print(rating)
        print(session['emp_id'])
        print(session['car_id'])
        push_review(des, rating)
    else:
        emp_id = request.args.get('emp_id')
        print(request.args)
        session['emp_id'] = request.args.get('emp_id')
        session['car_id'] = request.args.get('car_id')
        print(emp_id)
    return render_template('User/write_review.html')

@app.route('/reviews')
def reviews():
    data = fetch_reviews()
    print(data)
    return render_template('User/reviews.html', data = data)

@app.route('/backend-operation')
def backend_operation():
    # Perform backend operations here
    backend_data = "Backend operations performed successfully."
    print("lol")
    car_id = request.args.get('car_id')
    action = request.args.get('action')
    final_price = request.args.get('final_price')
    return redirect(url_for('wishlist', car_id=car_id, action=action, final_price=final_price))

def fetch_reviews():
    cur = mysql.connection.cursor()
    str = f"SELECT * FROM review WHERE for_emp_ID = {session['user_id']}"
    cur.execute(str)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata}")
    cur.close()
    return fetchdata

def push_review(des, rating):
    id = generate_review_id(des, rating)
    print(id)
    cur = mysql.connection.cursor()
    str_customer = f"INSERT INTO review VALUES('{id}',{rating},'{des}','{session['user_id']}',{session['car_id']},{session['emp_id']})"
    print(f"str_customer: {str_customer}")
    cur.execute(str_customer)
    mysql.connection.commit()
    cur.close()

def generate_review_id(des, rating):
    str = f"{des[:4]}_{rating}_{session['car_id']}_{des[-2:]}_{time.time()}"
    return str


def calc_emp_incentive():
    cur = mysql.connection.cursor()
    str = f"SELECT sale_involved_car_id FROM sale WHERE sale_by_emp_id = {session['user_id']}"
    cur.execute(str)
    fetchdata = cur.fetchall()
    list = []
    for ele in fetchdata:
        str = f"SELECT price FROM car_features WHERE car_ID = {ele[0]}"
        cur.execute(str)
        result = cur.fetchall()
        list.append(result[0][0])
    amount = 0
    for ele in list:
        amount = amount + 0.02*ele
    amount = amount*100000
    print(f"list: {amount}")
    cur.close()
    return amount

def get_sold_data():
    cur = mysql.connection.cursor()
    str = f"SELECT sale_involved_car_id, sale_date FROM sale WHERE sale_by_emp_id = {session['user_id']}"
    cur.execute(str)
    fetchdata = cur.fetchall()
    list = []
    for ele in fetchdata:
        str = f"SELECT car_name, image_link, price FROM car_features WHERE car_ID = {ele[0]}"
        cur.execute(str)
        result = cur.fetchall()
        list.append(result[0] + ele)
    print(f"list: {list}")
    cur.close()
    return list

def get_emp_data():
    cur = mysql.connection.cursor()
    str = f"SELECT * FROM employee WHERE emp_ID = {session['user_id']}"
    cur.execute(str)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata[0]}")
    cur.close()
    return fetchdata[0]

def customer_data():
    cur = mysql.connection.cursor()
    str = f"SELECT * FROM customer WHERE customer_ID = '{session['user_id']}'"
    cur.execute(str)
    fetchdata = cur.fetchall()
    print(f"fetchdata: {fetchdata[0]}")
    cur.close()
    return fetchdata[0]

def get_bought_car_data():
    cur = mysql.connection.cursor()
    str = f"SELECT sale_involved_car_id, sale_date, sale_by_emp_id FROM sale WHERE sale_to_cust_id = '{session['user_id']}'"
    cur.execute(str)
    fetchdata = cur.fetchall()
    list = []
    for ele in fetchdata:
        str = f"SELECT car_name, image_link, price FROM car_features WHERE car_ID = {ele[0]}"
        cur.execute(str)
        result = cur.fetchall()
        list.append(result[0] + ele)
    print(f"list: {list}")
    cur.close()
    return list


def get_car_data():
    # Fetch the details of all the cars from the "car_features" table
    return read_query("SELECT * FROM car_features")


def customerExists(email, password):
    """Checks if the customer exists in the "customer" table.

    Args:
        email (str): The customer's email.
        password (str): The customer's password.

    Returns:
        bool: True if the customer exists, False otherwise.
        str: The customer's ID if they exist, None otherwise.
    """

    customer_id = read_query(
        f"SELECT customer_ID from customer where Password = '{password}' and Email = '{email}'")

    return bool(customer_id), customer_id


def get_empid(email, password):

    # Check if the employee exists in the "employee" table
    fetchdata = read_query(
        f"SELECT emp_ID FROM employee WHERE Name = '{email}' and password = '{password}'")

    if fetchdata == ():  # no such employee
        return None

    # Return the employee ID
    emp_id = fetchdata[0][0]
    print(f"emp_id: {emp_id}")
    return emp_id


def get_wishlist_data():

    # Fetch the details of all the cars in the wishlist from the "car_ownership" table
    fetchdata = read_query(
        f"SELECT owned_car_id FROM car_ownership WHERE owner_cust_id = '{session['user_id']}'")

    car_details = []  # list of car details
    for car in fetchdata:  # each car in the wishlist
        for car_id in car:  # each car's ID

            # Fetch the details of the car from the "car_features" table
            fetchdata = read_query(
                f"SELECT car_name, image_link, price, car_ID FROM car_features WHERE car_ID = {car_id}")

            fetchdata = fetchdata[0]
            car_details.append(fetchdata)

    print(f"car_details: {car_details}")
    return car_details


def delete_appointment(app_id):
    # Delete the appointment from the "appointment" table
    write_query(f"DELETE FROM appointment WHERE app_ID = '{app_id}'")


def get_appointments(cust_id):
    # Generate the list of appointments to pass to the HTML file

    return read_query(f"SELECT Date, Time, Name, car_name, image_link, app_ID FROM appointment INNER JOIN car_features ON   appointment.Appointment_for_car_id = car_features.car_ID INNER JOIN employee ON appointment.handling_emp_id = employee.emp_ID WHERE appointment.booking_cust_id = '{cust_id}'")


def create_appointment(app_id, date, time, emp_id, cust_id, car_id):
    # Insert the new appointment into the "appointment" table
    write_query(
        f"INSERT INTO appointment VALUES('{app_id}','{date}','{time}',{emp_id},'{cust_id}',{car_id})")


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
    fetchdata = read_query("SELECT emp_ID FROM employee")

    emp_ids = [e[0] for e in fetchdata]
    print(f"emp_ids: {emp_ids}")
    chosen = random.randint(0, len(emp_ids)-1)
    return emp_ids[chosen]


if __name__ == "__main__":
    app.run(debug=True)
