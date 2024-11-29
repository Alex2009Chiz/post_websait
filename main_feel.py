

from flask import Flask, request, flash ,render_template
import sqlite3

app = Flask(__name__)
app.secret_key ='1234'
con = sqlite3.connect("date.bd", check_same_thread=False)
cursor = con.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS password_email
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 last_name TEXT,
                 name TEXT,
                 patronymic TEXT,
                 gender TEXT,
                 email TEXT,
                 username TEXT,
                 password TEXT)
                 """)

@app.route("/register/")
def register_page():
    return render_template("register.html")

@app.route("/login/")
def login():
    return render_template("login.html")

@app.route("/save_register/",methods=['POST','GET'])
def page_index():
    if request.method == 'POST':
        cursor.execute(
            "INSERT INTO password_email (last_name, name, patronymic, gender,  email, username, password) VALUES (?,?,?,?,?,?,?) ",
               (request.form['last_name'],
           request.form['name'],
           request.form['patronymic'],
           request.form['gender'],
           request.form['email'],
           request.form['username'],
           request.form['password']))
        con.commit()
        return 'регистрированние закончено'
    return 'зарегестрованный'

@app.route("/authorization/", methods=['POST','GET'])
def authorization_page():
    if request.method == 'POST':
        login = request.form['username']

        if cursor.execute('SELECT * FROM password_email  WHERE username=(?)',(login,)).fetchall() is True:
            flash('Вы авторизованны' ,'succerss')
            return render_template('authorization.html')
        else:
            flash('Неверный логин или пароль', 'danger')
            return render_template('authorization.html')
    return  render_template('authorization.html')




app.run(debug=True)
