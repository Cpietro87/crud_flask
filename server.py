from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__,  static_url_path= '/static' )
load_dotenv()
# Conneted MySQL
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') 
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') 

mysql = MySQL(app)

# Configuración de Flask-Login
app.secret_key = "mysecretkey"
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."

# Modelo de usuario
class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password



@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, email, password FROM users WHERE id = %s", (user_id,))
    user = cur.fetchone()
    cur.close()
    if user:
        return User(user[0], user[1], user[2])
    return None

# Router

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, email, password FROM users WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()
        cur.close()
        
        if user:
            user_obj = User(user[0], user[1], user[2])
            login_user(user_obj)
            flash('Login successful!', 'success')
            return redirect(url_for('data'))
        else:
            flash('Credenciales Invalidas', 'error')
    return render_template('login.html')

@app.route('/')
def main():
    return render_template('login.html')

# Grafícos
@app.route('/grafico')
def grafico():
    cur = mysql.connection.cursor()
    cur.execute('SELECT grupo, COUNT(*) FROM contact GROUP BY grupo')
    data = cur.fetchall()
    print(data)
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    return render_template('graph.html', labels=labels, values=values)

# Ruta de logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('has cerrado sesión')
    return redirect(url_for('login'))

# Read
@app.route('/data')
def data():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contact')
    data = cur.fetchall()
    return render_template( 'index.html', clientes = data)

@app.route('/save') 
def save():
    return render_template('save.html')


@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        grupo = request.form['grupo']
        print(grupo)
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO contact (fullname, phone, email, grupo) VALUES (%s,%s,%s,%s)", (fullname, phone, email, grupo))
            mysql.connection.commit()
            return redirect(url_for('data'))
        except Exception as e:
            return render_template('login.html')


@app.route('/edit/<id>')
def get_client(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contact WHERE id = %s', (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-cliente.html',contact= data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        grupo = request.form['grupo']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contact
            SET fullname = %s,
                email = %s,
                phone = %s,
                grupo = %s
            WHERE id = %s
        """, (fullname, email, phone, grupo, id))
        mysql.connection.commit()
        return redirect(url_for('data')) 
# Server
if __name__ == '__main__':
    app.run(port=5000, debug=True)