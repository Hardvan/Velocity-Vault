from flask import Flask, render_template, request, jsonify, redirect, session
from QR_OCR_Generator import generate_customer_id
from flask_mysqldb import MySQL
from datetime import date
import random


app = Flask(__name__)
app.secret_key = 'lololol898989'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'carshowroom'

logged_in = False
current_user_type = "blank"
customer_id = "none"
name = "none"

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def dashboard():
    cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO car_features VALUES('Swift Dzire', 2)")
    cur.execute("SELECT * FROM car_features")
    fetchdata = cur.fetchall()
    print(fetchdata)
    # mysql.connection.commit()
    cur.close()
    alert = False
    global current_user_id
    current_user_id = 0
    session['user_id'] = 0
    return render_template("User/Dashboard.html",
                           alert=alert, logged_in=logged_in,
                           current_user_id=current_user_id,
                           name=name)


@app.route('/index')
def index():
    print(session['user_id'])
    if session['user_id'] == 0:
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
    print(fetchdata)
    cur.close()
    return fetchdata


@app.route('/customerDashboard', methods=['GET', 'POST'])
def custLogin():
    global current_user_id
    bypass = request.args.get('bypass')

    if request.method == "POST":
        if 'sign_up' in request.form:
            print(request.form)
            alert = True
            action = "sign_up"
            customer_id = generate_customer_id(request.form['orangeForm-name'],
                                               request.form['orangeForm-age'], request.form['orangeForm-phone'])
            print(customer_id)
            print(date.today())
            cur = mysql.connection.cursor()
            # str = ("INSERT INTO customer VALUES({customer_id}, %s, %s, %s, %s, %s, %s)", customer_id, request.form['orangeForm-name'], request.form['orangeForm-age'], request.form['orangeForm-phone'], request.form['orangeForm-email'], date.today(), request.form['orangeForm-pass'])
            str_customer = "INSERT INTO customer VALUES('{}','{}', {}, {}, '{}', '{}', '{}')".format(
                customer_id, request.form['orangeForm-name'], request.form['orangeForm-age'], request.form['orangeForm-phone'], request.form['orangeForm-email'], date.today(), request.form['orangeForm-pass'])
            print(str_customer)
            cur.execute(str_customer)
            mysql.connection.commit()
            cur.close()
            current_user_id = customer_id
            print(current_user_id)
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
            if (customer_id == ()):
                logged_in = False
                alert = False
                return render_template("User/Dashboard.html", alert=alert, name="unsuccessful", action=action, logged_in=logged_in)

            current_user_id = customer_id[0][0]
            session['user_id'] = current_user_id
            print(current_user_id)
            print(customer_id)
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
    return render_template("User/Dashboard.html", alert=alert, name="customer", action=action, logged_in=logged_in)


@app.route('/employeeDashboard', methods=['GET', 'POST'])
def empLogin():

    if request.method == "POST":
        print(request.form)
        alert = True
        logged_in = True
        emp_ID = get_empid(request.form['email'], request.form['pass'])
        if emp_ID == None:
            logged_in = False
            alert = False
            return render_template("User/Dashboard.html", alert=alert, name="unsuccessful", action="login", logged_in=logged_in)
        session['user_id'] = emp_ID
    else:
        alert = False
    return render_template("User/Dashboard.html", alert=alert, name="employee", logged_in=logged_in)


def get_empid(email, password):
    s = f"SELECT emp_ID FROM employee WHERE Name = '{email}' and password = '{password}'"
    cur = mysql.connection.cursor()
    cur.execute(s)
    fetchdata = cur.fetchall()
    if fetchdata == ():
        return None
    print(fetchdata[0][0])
    cur.close()
    return fetchdata[0][0]


@app.route('/collections', methods=['GET', 'POST'])
def cars():
    return render_template("User/cars.html")


@app.route('/carDetails')
def carDetails():
    data = request.args.get('car_id')
    print(data)
    cur = mysql.connection.cursor()
    s = f"SELECT * FROM car_features WHERE car_ID = {data}"
    cur.execute(s)
    fetchdata = cur.fetchall()
    print(fetchdata)
    cur.close()
    return render_template("User/car_details.html", fetchdata=fetchdata[0])


@app.route('/wishlist')
def wishlist():
    if session['user_id'] == 0:
        alert = False
        global name
        name = "yamete_kudasai"
        return redirect("/")
    print(session['user_id'])
    car_id = request.args.get('car_id')
    action = request.args.get('action')
    print(car_id)
    print(action)
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
    print(fetchdata)
    cur.close()
    var = []
    for inner in fetchdata:
        for val in inner:
            cur = mysql.connection.cursor()
            s = f"SELECT car_name, image_link, price, car_ID FROM car_features WHERE car_ID = {val}"
            cur.execute(s)
            fetchdata = cur.fetchall()
            fetchdata = fetchdata[0]
            var.append(fetchdata)
            print(fetchdata)
            cur.close()
    print(var)
    return var


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
        print(car_id)
    print(session['user_id'])
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
    print(fetchdata)
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
    print(s)
    return s


def stemmed(date):
    s = ""
    for ch in date:
        if ch == 'T':
            break
        else:
            s += ch
    return s


def stem_time(date):
    s = ""
    flag = False
    for ch in date:
        if flag == True:
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
    print(lst)
    return lst[chosen]


if __name__ == "__main__":
    # test_connection()
    app.run(debug=True)
