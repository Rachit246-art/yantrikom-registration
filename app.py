from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'  # For flash messages

# Database setup
def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            year TEXT NOT NULL,
            branch TEXT NOT NULL,
            section TEXT NOT NULL,
            rollno TEXT NOT NULL,
            payment TEXT NOT NULL
        );
    ''')
    conn.close()

@app.route('/')
def home():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    year = request.form['year']
    branch = request.form['branch']
    section = request.form['section']
    rollno = request.form['rollno']
    payment = request.form['payment']

    if not name or not email or not year or not branch or not section or not rollno or not payment:
        flash("All fields are required!")
        return redirect('/')

    conn = sqlite3.connect('users.db')
    conn.execute(
        "INSERT INTO users (name, email, year, branch, section, rollno, payment) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (name, email, year, branch, section, rollno, payment)
    )
    conn.commit()
    conn.close()

    flash("Registration successful!")
    return redirect('/')

@app.route('/users')
# def show_users():
#     conn = sqlite3.connect('users.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT name, email, year, branch, section, rollno, payment FROM users")
#     users = cursor.fetchall()
#     conn.close()
#     return render_template('users.html', users=users)
def show_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, year, branch, section, rollno, payment FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
