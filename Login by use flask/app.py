from flask import Flask, render_template, request
import pyodbc
import bcrypt

app = Flask(__name__)

# SQL Server Connection - tera server name dal diya
conn_str = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-OJ5AJOP;"
    "DATABASE=loginDB;"
    "Trusted_Connection=yes;"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    conn=None
    try:
        
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Users table se email check kar
        cursor.execute("SELECT password FROM [login tabel] WHERE email = ?", (email,))
        row = cursor.fetchone()

        if row:
            db_password = row[0]
            # Abhi password plain hai table mein. Baad mein bcrypt se hash karenge
            if password == db_password:
                return "Login Success! Welcome " + email
            else:
                return "incorect password"
        else:
            return "Email not found"

    except Exception as e:
        return "Error: " + str(e)

    finally:
        if conn is not None:
           conn.close()

if __name__ == '__main__':
    app.run(debug=True)