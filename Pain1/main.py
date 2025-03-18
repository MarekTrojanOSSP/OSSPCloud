from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'tajny_klic'  # Klíč pro uložení session
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def init_db():
    conn = sqlite3.connect(r"C:\Users\BornyCZE\Documents\python-project-ossp\cloud-project\cloud.db")
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

@app.route('/registr', methods=['GET', 'POST'])
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(r"C:\Users\BornyCZE\Documents\python-project-ossp\cloud-project\cloud.db")
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM users WHERE email=? AND password=?", (email, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            return redirect(url_for(upload))
    else:
        return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            file_size = os.path.getsize(filepath)
            conn = sqlite3.connect(r"C:\Users\BornyCZE\Documents\python-project-ossp\cloud-project\cloud.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO files (user_id, file_name, file_size) VALUES (?, ?, ?)", 
                           (session['user_id'], filename, file_size))
    
    
    cursor.execute("SELECT file_name FROM files WHERE user_id=?", (session['user_id'],))
    files = cursor.fetchall()
    return render_template('upload.html', files=files)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        conn = sqlite3.connect(r"C:\Users\BornyCZE\Documents\python-project-ossp\cloud-project\cloud.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM files WHERE file_name=? AND user_id=?", (filename, session['user_id']))
        conn.commit()
    return redirect(url_for('upload'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
