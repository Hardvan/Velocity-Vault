from flask import Flask, render_template, request, jsonify, redirect, session
from QR_OCR_Generator import generate_customer_id
from flask_mysqldb import MySQL
from datetime import date
import stripe
import random


app = Flask(__name__)
app.secret_key = 'lololol898989'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'car_showroom'

#stripe api keys
stripe_keys = {
    "secret_key": "sk_test_51OqBUDSDxbyR6TDXKq1yk8FCTIRGukANTOgdCUyChhRf4YmoqubpGmDo0JSdxSkEMjxEklUIZECY61bRPzjlgFpD00yfhA9sr7",
    "publishable_key": "pk_test_51OqBUDSDxbyR6TDXyVusFbV7IChPwvs8PzdP6AXt65JSi9gObEyC66XB33oKuf4UvXSgaIk9gB8TqDmKQLrnlfFY00opHauWOd",
}

stripe.api_key = stripe_keys["secret_key"]

logged_in = False
current_user_type = "blank"
customer_id = "none"
name = "none"

mysql = MySQL(app)
@app.route('/', methods = ['GET','POST'])



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
    return render_template("User/Dashboard.html", alert = alert, logged_in = logged_in, current_user_id = current_user_id, name = name)

@app.route('/index')
def index():
    print(session['user_id'])
    if session['user_id'] == 0:
        alert = False
        global name
        name = "yamete_kudasai"
        return redirect("/")
    car_data = get_car_data()
    return render_template("index.html", car_data = car_data)

def get_car_data():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM car_features")
    fetchdata = cur.fetchall()
    print(fetchdata)
    cur.close()
    return fetchdata

@app.route('/customerDashboard', methods = ['GET','POST'])
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
            str_customer = "INSERT INTO customer VALUES('{}','{}', {}, {}, '{}', '{}', '{}')".format(customer_id, request.form['orangeForm-name'], request.form['orangeForm-age'], request.form['orangeForm-phone'], request.form['orangeForm-email'], date.today(), request.form['orangeForm-pass'])
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
            str_check_customer = "SELECT customer_ID from customer where Password = '{}' and Email = '{}'".format(request.form['pass'], request.form['email'])
            temp = "SELECT * FROM customer"
            cur.execute(str_check_customer)
            customer_id = cur.fetchall()
            if(customer_id == ()):
                logged_in = False
                alert = False
                return render_template("User/Dashboard.html", alert = alert, name = "unsuccessful", action = action, logged_in = logged_in)
            
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
    return render_template("User/Dashboard.html", alert = alert, name = "customer", action = action, logged_in = logged_in)

@app.route('/employeeDashboard', methods = ['GET','POST'])
def empLogin():

    if request.method == "POST":
        print(request.form)
        alert = True
        logged_in = True
        emp_ID = get_empid(request.form['email'], request.form['pass'])
        if emp_ID == None:
            logged_in = False
            alert = False
            return render_template("User/Dashboard.html", alert = alert, name = "unsuccessful", action = "login", logged_in = logged_in)
        session['user_id'] = emp_ID
    else:
        alert = False
    return render_template("User/Dashboard.html", alert = alert, name = "employee", logged_in = logged_in)

def get_empid(email, password):
    str = "SELECT emp_ID FROM employee WHERE Name = '{}' and password = '{}'".format(email, password)
    cur = mysql.connection.cursor()
    cur.execute(str)
    fetchdata = cur.fetchall()
    if fetchdata == ():
        return None
    print(fetchdata[0][0])
    cur.close()
    return fetchdata[0][0]



@app.route('/collections', methods = ['GET','POST'])
def cars():
    return render_template("User/cars.html")


@app.route('/carDetails')
def carDetails():
    data = request.args.get('car_id')
    print(data)
    cur = mysql.connection.cursor()
    str = "SELECT * FROM car_features WHERE car_ID = {}".format(data)
    cur.execute(str)
    fetchdata = cur.fetchall()
    print(fetchdata)
    cur.close()
    return render_template("User/car_details.html", fetchdata = fetchdata[0])

@app.route('/wishlist', methods = ['GET, POST'])
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
    if action == "1":
        cur = mysql.connection.cursor()
        
    if action == "0":
        cur = mysql.connection.cursor()
        str1 = "DELETE FROM car_ownership WHERE owner_cust_id = '{}' and owned_car_id = {}".format(session['user_id'], car_id)
        cur.execute(str1)
        mysql.connection.commit()
        cur.close()
    elif car_id != None:
        assign_emp_id = get_emp_ids()
        cur = mysql.connection.cursor()
        str2 = "INSERT INTO car_ownership VALUES('{}',{},{})".format(session['user_id'], car_id, assign_emp_id)
        cur.execute(str2)
        mysql.connection.commit()
        cur.close()
    data = get_data()
    return render_template("User/wishlist.html", data = data)

def get_data():
    cur = mysql.connection.cursor()
    str = "SELECT owned_car_id FROM car_ownership WHERE owner_cust_id = '{}'".format(session['user_id'])
    cur.execute(str)
    fetchdata = cur.fetchall()
    print(fetchdata)
    cur.close()
    var = []
    for inner in fetchdata:
        for val in inner:
            cur = mysql.connection.cursor()
            str = "SELECT car_name, image_link, price, car_ID FROM car_features WHERE car_ID = {}".format(val)
            cur.execute(str)
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


@app.route('/appointments', methods = ['GET','POST'])
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
    list = gen_list_to_pass(session['user_id'])
    return render_template("User/Appointments.html", list = list)

def delete_entry(app_id):
    cur = mysql.connection.cursor()
    str1 = "DELETE FROM appointment WHERE app_ID = '{}'".format(app_id)
    cur.execute(str1)
    mysql.connection.commit()
    cur.close()


def gen_list_to_pass(cust_id):
    str = "SELECT Date, Time, Name, car_name, image_link, app_ID FROM appointment INNER JOIN car_features ON   appointment.Appointment_for_car_id = car_features.car_ID INNER JOIN employee ON appointment.handling_emp_id = employee.emp_ID WHERE appointment.booking_cust_id = '{}'".format(cust_id)
    cur = mysql.connection.cursor()
    cur.execute(str)
    fetchdata = cur.fetchall()
    print(fetchdata)
    cur.close()
    return fetchdata
    

def plz_push_all(app_id, date, time, emp_id, cust_id, car_id):
    cur = mysql.connection.cursor()
    str2 = "INSERT INTO appointment VALUES('{}','{}','{}',{},'{}',{})".format(app_id, date, time, emp_id, cust_id, car_id)
    cur.execute(str2)
    mysql.connection.commit()
    cur.close()

def gib_app_id_plz(cust_id, car_id, date):
    str = cust_id[:4] + "_" + car_id + date[-2:]
    print(str)
    return str

def stemmed(date):
    str = ""
    for char in date:
        if char == 'T':
            break
        else:
            str = str+char
    return str

def stem_time(date):
    str = ""
    flag = False
    for char in date:
        if flag == True:
            str = str+char
        if char == 'T':
            flag = True
    return str

def get_emp_ids():
    cur = mysql.connection.cursor()
    str = "SELECT emp_ID FROM employee"
    cur.execute(str)
    fetchdata = cur.fetchall()
    cur.close()
    list = []
    for ele in fetchdata:
        list.append(ele[0])
    length = len(list)
    chosen = random.randint(0,length-1)
    print(list)
    return list[chosen]

if __name__ == "__main__":
    #test_connection()
    app.run(debug=True)
