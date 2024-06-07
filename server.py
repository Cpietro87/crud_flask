from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os


app = Flask(__name__,  static_url_path= '/static' )
load_dotenv()
# Conección MySQL
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') 
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') 

mysql = MySQL(app)

#Rutas

@app.route('/login')
def main():
    return render_template('login.html')

@app.route('/')# App Web
def data():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contact')
    data = cur.fetchall()
    return render_template( 'index.html', clientes = data)


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
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contact
            SET fullname = %s,
                email = %s,
                phone = %s
            WHERE id = %s
        """, (fullname, email, phone, id))
        mysql.connection.commit()
        return redirect(url_for('data')) 



# Server
if __name__ == '__main__':
    app.run(port=5000, debug=True)