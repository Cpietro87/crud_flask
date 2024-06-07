from flask import Flask, render_template
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


# Server
if __name__ == '__main__':
    app.run(port=5000, debug=True)