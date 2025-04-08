from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import sqlite3
import os

app=Flask(__name__)


USERNAME = "administrator_of_the_cloud"
PASSWORD = "4dm1n1str4t0r_0f_th3_cl0ud"

@app.route("/login",methods=['GET','POST'])
def login():
   if request.method == "POST":
       username = request.form.get('username')
       password = request.form.get('psw')

       print(username,password)

       if username == USERNAME and password == PASSWORD:
           return redirect(url_for('welcome'))
       else:
           return redirect(url_for('login'))
   return render_template('login.html')

@app.route('/registr', methods=['GET', 'POST'])
def registr():
  if request.method == 'POST':
      username = request.form['username']
      password = request.form['psw']

      conn = sqlite3.connect("cloud.db")
      cursor = conn.cursor()
      cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                     (username, password))
      conn.commit()
      conn.close()

      return redirect(url_for('login'))  # Přesměrování na přihlášení
  return render_template('registr.html')

@app.route('/')
def index():
   return render_template('index.html')
@app.route('/welcome')
def welcome():
   return render_template('welcome.html')
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

if __name__ == '__main__':
    """init_db()"""
    app.run(debug=True)