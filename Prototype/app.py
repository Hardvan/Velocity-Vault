from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'carshowroom'

mysql = MySQL(app)
@app.route('/')

def dashboard():
    cur = mysql.connection.cursor()
    # cur.execute("INSERT INTO car_features VALUES('Swift Dzire', 2)")
    cur.execute("SELECT * FROM car_features")
    fetchdata = cur.fetchall()
    print(fetchdata)
    # mysql.connection.commit()
    cur.close()
    return render_template("User/Dashboard.html")

@app.route('/index')
def index():
    return render_template("login.html")


@app.route('/customerLogin')
def custLogin():
    return render_template("User/customerLogin.html")

@app.route('/employeeLogin')
def empLogin():
    return render_template("User/employeeLogin.html")
if __name__ == "__main__":
    #test_connection()
    app.run(debug=True)
