from flask import Flask, render_template, request, redirect, url_for, session
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
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
''')

# Create the 'files' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    file_name TEXT NOT NULL,
    file_size INTEGER NOT NULL,  -- Size in bytes
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')

# Commit changes and close the connection
conn.commit()

# Optionally, insert some sample data
cursor.execute("INSERT INTO users (username, email, password) VALUES ('pan_Mychail', 'michal.bornhorst@student.ossp.cz', 'password')")
cursor.execute("INSERT INTO users (username, email, password) VALUES ('pan_Marek', 'marek.trojan@student.ossp.cz', 'password')")
cursor.execute("INSERT INTO users (username, email, password) VALUES ('pan_Illja', 'illja.perunov@student.ossp.cz', 'password')")
# Commit and close
conn.commit()
conn.close()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registr.html', methods=['GET', 'POST'])
def registr():
     if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("cloud.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                       (username, email, password))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))  # Přesměrování na přihlášení

    return render_template('registr.html')

@app.route('/Login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect("cloud.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for('upload'))
        else:
            return "Špatné přihlašovací údaje!"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
