from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'tajny_klic'  # Klíč pro uložení session
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def init_db():
    conn = sqlite3.connect("cloud.db")
    cursor = conn.cursor()
    # Create the 'users' table
    cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
""")


    # Commit changes and close the connection
    """conn.commit()

    # Optionally, insert some sample data
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('pan_Mychail', 'password')")
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('pan_Marek', 'password')")
    cursor.execute(
        "INSERT INTO users (username, password) VALUES ('pan_Illja',  'password')")
    # Commit and close"""

    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/neco')
def neco():
    return render_template('neco.html')

@app.route('/registr', methods=['GET', 'POST'])
def registr():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect("cloud.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))  # Přesměrování na přihlášení
    return render_template('registr.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['psw']


        conn = sqlite3.connect("cloud.db")

        cursor = conn.cursor()

        user = "";

        try:
            # Execute query
            cursor.execute("SELECT username, password FROM users")

            # Fetch results
            user = cursor

            if user:
                print("User found:", user)
            else:
                print("No user found with those credentials")

        except sqlite3.Error as e:
            print("Database error:", e)
        finally:
            # Close connection
            conn.close()


        if user:
            session['username'] = user[0]
            return redirect(url_for("neco"))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)