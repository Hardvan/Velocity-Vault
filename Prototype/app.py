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
import threading
import mail

# Custom modules
from QR_Generator import generate_customer_id, generate_employee_id, save_qr_code
from QR_Reader import read_qr_code
from CRUD_QR import add_qr_code, get_qr_code, update_qr_code, delete_qr_code
from HuggingFace import sentiment_analysis, summarize_text
from password_manager import hash_password, check_password
import whatsapp_message
from save_qr_image import save_qr_image

# Load the environment variables
import os
from dotenv import load_dotenv
load_dotenv()

# Flask app
app = Flask(__name__)

# * SQL Configuration
app.secret_key = 'lololol898989'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car_showroom'
mysql = MySQL(app)

# * User variables
logged_in = False  # ? True/False: User is logged in or not
current_user_type = "blank"  # ? "customer"/"employee": Type of the current user
customer_id = "none"  # ? ID of the current customer
name = "none"  # ? Name of the current user

# * Stripe keys
stripe_keys = {
    "secret_key": os.getenv("STRIPE_SECRET_KEY"),
    "publishable_key": "pk_test_51OqBUDSDxbyR6TDXyVusFbV7IChPwvs8PzdP6AXt65JSi9gObEyC66XB33oKuf4UvXSgaIk9gB8TqDmKQLrnlfFY00opHauWOd",
}
stripe.api_key = stripe_keys["secret_key"]


# * MongoDB setup
mongo_db = None
mongo_collection = None
mongodb_uri = os.getenv("MONGODB_URI")
client = MongoClient(mongodb_uri, server_api=ServerApi('1'))
# Select the database and collection
mongo_db = client['DBMS_db']
mongo_collection = mongo_db['qr_codes']


# Testing Parameters
TEST_CONNECTION = True  # ? Test/Don't test the connection to MongoDB
TEST_CRUD_QR_CODE = True  # ? Test/Don't test the CRUD operations for the QR codes

# WhatsApp & Email Parameters
WHATSAPP = True  # ? Send/Don't send the WhatsApp message


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




if TEST_CRUD_QR_CODE:

    print("=== Testing CRUD Operations for QR Codes ===")

    user_id = 'charlie_3210_2757'
    image_path = './QR_ID_Customer/charlie_3210_2757.png'

    # Create
    add_qr_code(user_id, image_path, 'C', mongo_collection)

    # Read
    qr_code = get_qr_code(user_id, mongo_collection)
    print("Retrieved data:")
    print(f"User ID: {qr_code['user_id']}")
    print(f"User: {qr_code['user']}")
    save_qr_image(qr_code['image'], user_id + "_retrieved.png")

    # Update
    update_qr_code(user_id, image_path, mongo_collection)

    # Delete
    delete_qr_code(user_id, mongo_collection)

    print("=== CRUD Operations for QR Codes Test Completed ===")


# HTML File variables
dashboard_html = "dashboard.html"


# SQL Functions
def read_query(query):
    """Executes a SELECT query on the database.
    This function greatly simplifies the process of executing a query
    by reducing the no. of lines of code required and improving readability.

    Args
    ----
    - `query`: The SQL query string to execute.

    Performs
    --------
    - Executes the query
    - Fetches the result
    - Closes the cursor

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
    - `query`: The SQL query string to execute.

    Performs
    --------
    - Executes the query
    - Commits the changes
    - Closes the cursor
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
# /emp_profile: Displays the employee profile page
# /enter_review: Allows the user to enter a review
# /reviews: Displays the reviews page
# /backend-operation: Performs backend operations
# /analysis: Displays the analysis page


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    """Main dashboard of the website.
    It is the first page that the user sees when they visit the website.
    It displays the main features of the website and allows the user to navigate to different pages.
    """

    print("=== In the Main Dashboard ===")

    # Load customer and employee tables, fill "Encrypted_Password" column if it has value 'NA'
    FILL_ENCRYPTED_PASSWORDS = True
    if FILL_ENCRYPTED_PASSWORDS:
        print("=== Filling Encrypted Passwords ===")

        # Fetch the details of all the customers from the "customer" table
        customers = read_query(
            "SELECT customer_ID, Password, Encrypted_Password FROM customer")
        # Fill the "Encrypted_Password" column in the "customer" table
        print("Filling Encrypted Passwords in the 'customer' table...")
        for customer in customers:
            customer_id = customer[0]
            password = customer[1]
            encrypted_password = customer[2]

            if encrypted_password == 'NA':
                write_query(
                    f"UPDATE customer SET Encrypted_Password = '{hash_password(password)}' WHERE customer_ID = '{customer_id}'")

        # Fetch the details of all the employees from the "employee" table
        employees = read_query(
            "SELECT emp_ID, password, Encrypted_Password FROM employee")
        # Fill the "Encrypted_Password" column in the "employee" table
        print("Filling Encrypted Passwords in the 'employee' table...")
        for employee in employees:
            emp_id = employee[0]
            password = employee[1]
            encrypted_password = employee[2]

            if encrypted_password == 'NA':
                write_query(
                    f"UPDATE employee SET Encrypted_Password = '{hash_password(password)}' WHERE emp_ID = '{emp_id}'")

        print("✅ Filled the 'Encrypted_Password' column in the 'customer' and 'employee' tables.")

    alert = False  # ? True/False: Alert message is displayed or not
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

    print("=== In the Index Page ===")

    print(f"session['user_id']: {session['user_id']}")
    if session['user_id'] == 0:  # user is not logged in
        global name
        name = "dummy_name"  # dummy name
        return redirect("/")

    car_data = get_car_data()
    print("✅ Fetched the car data.")
    return render_template("index.html", car_data=car_data)


@app.route('/customerDashboard', methods=['GET', 'POST'])
def custLogin():
    """Customer login/signup page.
    After the user logs in or signs up, they are redirected to this page.
    """

    print("=== In the Customer Dashboard ===")

    global current_user_id
    bypass = request.args.get('bypass')  # 0: Bypass the login/signup page

    if request.method == "POST":
        # * Signing up the user
        if 'sign_up' in request.form:
            print("Signing up the user...")
            print(f"request.form: {request.form}")
            name = request.form['orangeForm-name']
            age = request.form['orangeForm-age']
            phone = request.form['orangeForm-phone']
            email = request.form['orangeForm-email']
            password = request.form['orangeForm-pass']

            alert = True
            action = "sign_up"
            customer_id = generate_customer_id(name, age, phone)
            print(f"Generated customer_id: {customer_id}")
            print(f"date.today(): {date.today()}")

            # Insert the new customer into the "customer" table
            write_query(
                f"INSERT INTO customer VALUES('{customer_id}','{name}', {age}, {phone}, '{email}', '{date.today()}', '{password}', '{hash_password(password)}')")
            print("✅ Inserted the new customer into the 'customer' table.")

            # Create the QR code of the customer & add it to MongoDB collection "qr_codes"
            image_path = save_qr_code(
                customer_id, user="C", folder="QR_ID_Customer")
            add_qr_code(customer_id, image_path, "C", mongo_collection)
            print("✅ Added the new QR code to the collection.")

            # Save the customer ID in the session
            current_user_id = customer_id
            print(f"current_user_id: {current_user_id}")
            session['user_id'] = current_user_id
            logged_in = True

            text = f"""Congratulations 🎉! You have successfully Created Your Velocity Vault Account.

Here are your credentials ->
    Username: {name}
    Password: {password}

This E-mail/ number will be used for all official communications from our platform
"""
            t_whatsapp = threading.Thread(
                target=ThreadSendWhatsapp, args=(text, ""))
            t_whatsapp.start()

        # * Logging in the user
        else:
            print("Logging in the user...")
            print(f"request.form: {request.form}")
            email = request.form['email']
            password = request.form['pass']

            alert = True
            action = "login"

            # Check if the customer exists in the "customer" table
            exists, customer_id = customerExists(email)
            if not exists:
                print("❌ Customer does not exist.")
                logged_in = False
                alert = False
                return render_template(dashboard_html,
                                       alert=alert, name="unsuccessful",
                                       action=action, logged_in=logged_in)

            # Check if the password is correct
            if not check_cust_password(password, customer_id[0][0]):
                print("❌ Incorrect password. Does not match.")
                logged_in = False
                alert = False
                return render_template(dashboard_html,
                                       alert=alert, name="unsuccessful",
                                       action=action, logged_in=logged_in)

            # Login successful
            print("✅ Customer Login successful.")
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
    qr_code = get_qr_code(current_user_id, mongo_collection)
    qr_image = qr_code['image']
    print("✅ Retrieved the QR code of the customer")

    # Save the QR code image
    image_path = f"QR_ID_Customer/{current_user_id}.png"
    save_qr_image(qr_image, image_path)

    # Read the QR code image
    qr_data = read_qr_code(image_path)
    print("✅ Read the data from the QR code.")

    # Delete the QR code image
    os.remove(image_path)

    return render_template(dashboard_html,
                           alert=alert, name="customer",
                           action=action, logged_in=logged_in,
                           qr_image=qr_image, qr_data=qr_data)


@app.route('/employeeDashboard', methods=['GET', 'POST'])
def empLogin():

    print("=== In the Employee Dashboard ===")

    if request.method == "POST":
        print("Logging in the employee...")
        print(f"request.form: {request.form}")
        email = request.form['email']
        password = request.form['pass']

        alert = True
        logged_in = True

        emp_id = get_empid(email, password)
        if emp_id == None:  # Login unsuccessful
            print("❌ Login unsuccessful as emp_id is None.")
            logged_in = False
            alert = False
            return render_template(dashboard_html,
                                   alert=alert, name="unsuccessful",
                                   action="login", logged_in=logged_in)

        print("✅ Employee Login successful.")
        session['user_id'] = emp_id
    else:
        alert = False

    return render_template(dashboard_html,
                           alert=alert, name="employee",
                           logged_in=logged_in)


@app.route('/collections', methods=['GET', 'POST'])
def cars():

    print("=== In the Cars Collection Page ===")
    return render_template("cars.html")


@app.route('/carDetails')
def carDetails():

    print("=== In the Car Details Page ===")

    data = request.args.get('car_id')
    print(f"data: {data}")

    # Fetch the details of the selected car from "car_features" table
    fetchdata = read_query(f"SELECT * FROM car_features WHERE car_ID = {data}")
    print("✅ Fetched the car details.")

    car_details = fetchdata[0]  # first car's details
    print(f"car_details: {car_details}")

    return render_template("car_details.html", fetchdata=car_details)


@app.route('/wishlist')
def wishlist():

    print("=== In the Wishlist Page ===")

    if session['user_id'] == 0:  # user is not logged in
        print("User is not logged in.")
        alert = False
        global name
        name = "dummy_name"
        return redirect("/")

    print(f"session['user_id']: {session['user_id']}")
    car_id = request.args.get('car_id')
    action = request.args.get('action')
    mode = request.args.get('mode')
    print(f"car_id: {car_id}")
    print(f"action: {action}")

    if action == "1":  # buy the car from the wishlist
        print("Buying the car from the wishlist...")
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
        car_name = get_car_name(car_id)
        emp_name = get_emp_name(sale_by_emp_id)
        customer_name = get_cust_name(sale_to_cust_id)

        write_query(
            f"DELETE FROM car_ownership WHERE owner_cust_id = '{session['user_id']}' and owned_car_id = {car_id}")
        write_query(
            f"INSERT INTO sale VALUES('{sale_id}','{sale_date}',{final_price},'{payment_method}','{sale_to_cust_id}',{sale_by_emp_id},{sale_involved_car_id})")
        print("✅ Bought the car from the wishlist.")

        # Send a WhatsApp message using a thread
        if WHATSAPP:
            path = get_url(car_id)
            text = f"""Congratulations 🎉! You have successfully bought the car. The details are:

*Customer Name*: {customer_name}
*Car Name*: {car_name}
*Employee Name*: {emp_name}
*Final Price*: {final_price}
*Payment Method*: {payment_method}
*Sale Date*: {sale_date}
*Sale ID*: {sale_id}
*Sale To Customer ID*: {sale_to_cust_id}
*Sale By Employee ID*: {sale_by_emp_id}
*Sale Involved Car ID*: {sale_involved_car_id}
"""
            t_whatsapp = threading.Thread(
                target=ThreadSendWhatsapp, args=(text, path))
            t_whatsapp.start()

    elif action == "0":  # delete the car from the wishlist
        write_query(
            f"DELETE FROM car_ownership WHERE owner_cust_id = '{session['user_id']}' and owned_car_id = {car_id}")
        print("✅ Deleted the car from the wishlist.")
    elif car_id != None:  # add the car to the wishlist
        assign_emp_id = get_emp_ids()
        write_query(
            f"INSERT INTO car_ownership VALUES('{session['user_id']}',{car_id},{assign_emp_id})")
        print("✅ Added the car to the wishlist.")

    data = get_wishlist_data()
    return render_template("wishlist.html", data=data, key=stripe_keys['publishable_key'])


def get_url(car_id):
    fetchdata = read_query(
        f"SELECT image_link FROM car_features WHERE car_ID = {car_id}")
    print(fetchdata[0][0])
    return fetchdata[0][0]


def ThreadSendWhatsapp(text, path):
    """Send the text message to WhatsApp using a thread to prevent the program from freezing.

    Args
    ----
    - `text`: The message to be sent.
    - `path`: The path of the image to be sent.
    """
    if path == "":
        mail.send_emails_account_created(text)
    else:
        mail.send_emails_sale_confirmed(text, path)
    whatsapp_message.SendMessage(text)


def gen_sale_id(cust_id, car_id, emp_id):
    sale_id = f"{cust_id[:4]}_{car_id}_{emp_id}_{date.today()}_{time.time()}"
    print(f"sale_id: {sale_id}")
    return sale_id


def get_emp_who_sold(cust_id, car_id):
    fetchdata = read_query(
        f"SELECT emp_ID FROM car_ownership where owner_cust_id = '{cust_id}' and owned_car_id = {car_id}")
    emp_id = fetchdata[0][0]
    return emp_id


def get_car_name(car_id):
    fetchdata = read_query(
        f"SELECT car_name FROM car_features WHERE car_ID = {car_id}")
    return fetchdata[0][0]


def get_emp_name(emp_id):
    fetchdata = read_query(
        f"SELECT Name FROM employee WHERE emp_ID = {emp_id}")
    return fetchdata[0][0]


def get_cust_name(cust_id):
    fetchdata = read_query(
        f"SELECT Name FROM customer WHERE customer_ID = '{cust_id}'")
    return fetchdata[0][0]


@app.route('/charge', methods=['POST'])
def charge():

    print("=== In the Charge Page ===")

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
    return render_template("sales.html", data=data)


def get_sale_data(emp_id):
    fetchdata = read_query(
        f"SELECT car_name, Name, final_price, sale_date, payment_method, image_link FROM sale INNER JOIN customer ON sale_to_cust_id = customer_ID INNER JOIN car_features ON sale_involved_car_id = car_ID WHERE sale_by_emp_id = {emp_id}")
    return fetchdata


@app.route('/profile')
def profile():

    print("=== In the Profile Page ===")

    cust_data = customer_data()
    bought_data = get_bought_car_data()
    return render_template("profile_user.html", cust_data=cust_data, bought_data=bought_data)


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():

    print("=== In the Appointments Page ===")

    temp_app_id = request.args.get('app_id')
    bypass = request.args.get('action')

    if bypass == "0":  # delete the appointment
        delete_appointment(temp_app_id)
        print("✅ Deleted the appointment.")

    if session['user_id'] == 0:  # user is not logged in
        print("User is not logged in.")
        global name
        name = "dummy_name"
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
        print("✅ Created a new appointment.")

        print(f"{date} : {time}")
        print(f"car_id: {car_id}")

    print(f"session['user_id']: {session['user_id']}")
    appointments_list = get_appointments(session['user_id'])

    return render_template("appointments.html", list=appointments_list)


@app.route('/emp_profile')
def emp_profile():

    print("=== In the Employee Profile Page ===")

    emp_data = get_emp_data()
    dept_name = get_dept_name(emp_data[5])
    sold_data = get_sold_data()
    incentive = calc_emp_incentive()
    return render_template('profile_employee.html', emp_data=emp_data,
                           dept_name=dept_name, sold_data=sold_data, incentive=incentive)


@app.route('/enter_review', methods=['GET', 'POST'])
def enter_review():

    print("=== In the Enter Review Page ===")

    if request.method == 'POST':  # Push the review
        des = request.form['des']
        rating = request.form['rating']
        print(f"des: {des}")
        print(f"rating: {rating}")
        print(f"emp_id: {session['emp_id']}")
        print(f"car_id: {session['car_id']}")
        push_review(des, rating)
        print("✅ Pushed the review.")
    else:  # Display the review form
        emp_id = request.args.get('emp_id')
        print(f"request.args: {request.args}")
        session['emp_id'] = request.args.get('emp_id')
        session['car_id'] = request.args.get('car_id')
        print(f"emp_id: {emp_id}")

    return render_template('write_review.html')


@app.route('/reviews')
def reviews():

    print("=== In the Reviews Page ===")

    data = fetch_reviews()
    print("✅ Fetched the reviews.")
    print(f"data: {data}")
    return render_template('reviews.html', data=data)


@app.route('/backend-operation')
def backend_operation():
    # Perform backend operations here
    print("=== In the Backend Operation Page ===")
    backend_data = "Backend operations performed successfully."
    car_id = request.args.get('car_id')
    action = request.args.get('action')
    final_price = request.args.get('final_price')
    return redirect(url_for('wishlist', car_id=car_id, action=action, final_price=final_price))


@app.route('/analysis')
def analysis():
    """
    Uses nested SQL Queries to perform various permutations & combinations of the data analysis such as:
    - `Basic Statistics`
        - Total Employees
        - Total Customers
        - Total Cars in Stock
        - Average Price of Cars
        - Total Cars Sold
        - Total Cars in Wishlist
        - Total Sales
        - Total Revenue
        - Total Appointments

    - `Advanced Statistics`
        - Most Sold Car
        - Most Sold Car by a Particular Employee
        - Customer with most cars in Wishlist
        - Customer with most cars bought
        - Employee with most sales
        - Employee with most appointments
    """

    statistics = {}

    # * Basic Statistics

    # Total Employees
    statistics["total_employees"] = read_query(
        "SELECT COUNT(*) FROM employee")[0][0]

    # Total Customers
    statistics["total_customers"] = read_query(
        "SELECT COUNT(*) FROM customer")[0][0]

    # Total Cars in Stock
    statistics["total_cars"] = read_query(
        "SELECT COUNT(*) FROM car_features")[0][0]

    # Average Price of Cars
    statistics["avg_price"] = read_query(
        "SELECT AVG(price) FROM car_features")[0][0]

    # Total Cars Sold
    statistics["total_cars_sold"] = read_query(
        "SELECT COUNT(*) FROM sale")[0][0]

    # Total Cars in Wishlist
    statistics["total_wishlist_cars"] = read_query(
        "SELECT COUNT(*) FROM car_ownership")[0][0]

    # Total Sales
    statistics["total_sales"] = read_query(
        "SELECT COUNT(*) FROM sale")[0][0]

    # Total Revenue
    statistics["total_revenue"] = read_query(
        "SELECT SUM(final_price) FROM sale")[0][0]

    # Total Appointments
    statistics["total_appointments"] = read_query(
        "SELECT COUNT(*) FROM appointment")[0][0]

    # * Advanced Statistics

    # Most Sold Car
    statistics["most_sold_car"] = read_query(
        "SELECT car_name, COUNT(sale_involved_car_id) FROM sale INNER JOIN car_features ON sale_involved_car_id = car_ID GROUP BY sale_involved_car_id ORDER BY COUNT(sale_involved_car_id) DESC LIMIT 1")[0]

    # Most Sold Car by a Particular Employee
    statistics["most_sold_car_by_emp"] = read_query(
        "SELECT Name, COUNT(sale_involved_car_id) FROM sale INNER JOIN employee ON sale_by_emp_id = emp_ID GROUP BY sale_by_emp_id ORDER BY COUNT(sale_involved_car_id) DESC LIMIT 1")[0]

    # Customer with most cars in Wishlist
    temp = read_query(
        "SELECT owner_cust_id, COUNT(owned_car_id) FROM car_ownership GROUP BY owner_cust_id ORDER BY COUNT(owned_car_id) DESC LIMIT 1")
    if temp == ():
        statistics["cust_most_wishlist"] = temp
    else:
        statistics["cust_most_wishlist"] = temp[0]

    # Customer with most cars bought
    var = read_query(
        "SELECT sale_to_cust_id, COUNT(sale_involved_car_id) FROM sale GROUP BY sale_to_cust_id ORDER BY COUNT(sale_involved_car_id) DESC LIMIT 1")[0]

    statistics["cust_name"] = (read_query(
        f"SELECT Name from customer where customer_ID = '{var[0]}'")[0][0], var[1])

    # Employee with most sales
    var = read_query(
        "SELECT sale_by_emp_id, COUNT(sale_involved_car_id) FROM sale GROUP BY sale_by_emp_id ORDER BY COUNT(sale_involved_car_id) DESC LIMIT 1")[0]

    statistics["best_emp"] = (read_query(
        f"SELECT Name from employee where emp_ID = '{var[0]}'")[0][0], var[1])

    # Number of Reviews
    statistics["count_reviews"] = read_query(
        "SELECT COUNT(*) FROM review")[0][0]

    # most wishlisted car
    varz = read_query(
        "SELECT owned_car_id, COUNT(*) AS frequency FROM car_ownership GROUP BY owned_car_id ORDER BY frequency DESC LIMIT 1;")[0]
    statistics["most_wish"] = (read_query(
        f"SELECT car_name from car_features where car_ID = '{varz[0]}'")[0][0], varz[1])

    # Employee with most appointments
    statistics["emp_most_appointments"] = read_query(
        "SELECT handling_emp_id, COUNT(app_ID) FROM appointment GROUP BY handling_emp_id ORDER BY COUNT(app_ID) DESC LIMIT 1")[0]

    print("✅ Successfully performed the data analysis.")
    print(f"statistics: {statistics}")

    return render_template("admin.html", statistics=statistics)


def fetch_reviews():
    return read_query(f"SELECT * FROM review WHERE for_emp_ID = {session['user_id']}")


def push_review(des, rating):
    des = des.replace("'", " ")
    review_id = generate_review_id(des, rating)
    s = sentiment_analysis(des)
    sentiment = s['label']
    sentiment_score = s['score']
    sentiment_score = round(sentiment_score*100)
    s2 = summarize_text(des)
    summarized_text = s2['summary_text']
    # Replace ' to avoid SQL syntax errors

    print(f"sentiment: {sentiment}")
    print(f"sentiment_score: {sentiment_score}")
    print(f"summarized_text: {summarized_text}")

    write_query(
        f"INSERT INTO review VALUES('{review_id}',{rating},'{des}','{session['user_id']}',{session['car_id']},{session['emp_id']},'{sentiment}','{sentiment_score}','{summarized_text}')")


def generate_review_id(des, rating):
    return f"{des[:4]}_{rating}_{session['car_id']}_{des[-2:]}_{time.time()}"


def calc_emp_incentive():
    fetchdata = read_query(
        f"SELECT sale_involved_car_id FROM sale WHERE sale_by_emp_id = {session['user_id']}")
    lst = []
    for ele in fetchdata:
        result = read_query(
            f"SELECT price FROM car_features WHERE car_ID = {ele[0]}")
        lst.append(result[0][0])
    amount = 0
    print(f"lst: {lst}")
    for ele in lst:
        amount += 0.02 * ele
    amount *= 100000
    print(f"amount: {amount}")

    return amount


def get_sold_data():
    fetchdata = read_query(
        f"SELECT sale_involved_car_id, sale_date FROM sale WHERE sale_by_emp_id = {session['user_id']}")
    lst = []
    for ele in fetchdata:
        result = read_query(
            f"SELECT car_name, image_link, price FROM car_features WHERE car_ID = {ele[0]}")
        lst.append(result[0] + ele)
    print(f"lst: {lst}")
    return lst


def get_emp_data():
    fetchdata = read_query(
        f"SELECT * FROM employee WHERE emp_ID = {session['user_id']}")
    return fetchdata[0]


def get_dept_name(dept_id):
    fetchdata = read_query(
        f"SELECT Name FROM department WHERE dept_ID = {dept_id}")
    return fetchdata[0][0]


def customer_data():
    fetchdata = read_query(
        f"SELECT * FROM customer WHERE customer_ID = '{session['user_id']}'")
    print(f"Customer data fetched: {fetchdata}")
    return fetchdata[0]


def get_bought_car_data():
    fetchdata = read_query(
        f"SELECT sale_involved_car_id, sale_date, sale_by_emp_id FROM sale WHERE sale_to_cust_id = '{session['user_id']}'")
    lst = []
    for ele in fetchdata:
        result = read_query(
            f"SELECT car_name, image_link, price FROM car_features WHERE car_ID = {ele[0]}")
        lst.append(result[0] + ele)
    print(f"lst: {lst}")
    return lst


def get_car_data():
    # Fetch the details of all the cars from the "car_features" table
    return read_query("SELECT * FROM car_features")


def customerExists(email):
    """Checks if the customer exists in the "customer" table.

    Args:
        email (str): The customer's email.

    Returns:
        bool: True if the customer exists, False otherwise.
        str: The customer's ID if they exist, None otherwise.
    """

    customer_id = read_query(
        f"SELECT customer_ID from customer where Email = '{email}'")
    print(f"customer_id: {customer_id}")

    return bool(customer_id), customer_id


def check_cust_password(password, customer_id):
    """Checks if the password is correct for the customer.

    Args:
        password (str): The password entered by the customer.
        customer_id (str): The customer's ID.

    Returns:
        bool: True if the password is correct, False otherwise.
    """

    fetchdata = read_query(
        f"SELECT Encrypted_Password FROM customer WHERE customer_ID = '{customer_id}'")
    return check_password(password, fetchdata[0][0])


def get_empid(email, password):

    print(f"email: {email}")
    print(f"password: {password}")
    # Check if the employee exists in the "employee" table
    fetchdata = read_query(
        f"SELECT emp_ID, Encrypted_Password FROM employee WHERE Name = '{email}'")

    if fetchdata == ():  # no such employee
        return None

    # Check if the password is correct
    if not check_password(password, fetchdata[0][1]):
        print("❌ Incorrect password. Does not match.")
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
