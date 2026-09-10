import os
import sqlite3
from datetime import timedelta
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='Templates', static_folder='.')
app.secret_key = 'skillup-portal-super-secret-key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=14)

DB_NAME = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            fullname TEXT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()

    default_presets = [
        ('student', 'Trainee Alex', 'TRN-2026-001', 'trainee@skillup.gov.in', 'password123'),
        ('govt', 'Director Sairam', 'MSDE-DIR-901', 'officer@skillup.gov.in', 'govpass2026'),
        ('employer', 'HR Manager', 'DELOITTE-REC', 'recruiter@deloitte.com', 'hirepass2026')
    ]
    for role, fullname, username, email, raw_pw in default_presets:
        cursor.execute('SELECT id FROM users WHERE email = ?', (email,))
        if not cursor.fetchone():
            cursor.execute(
                'INSERT INTO users (role, fullname, username, email, password) VALUES (?, ?, ?, ?, ?)',
                (role, fullname, username, email, generate_password_hash(raw_pw))
            )
    conn.commit()
    conn.close()

init_db()

@app.route('/')
@app.route('/index.html')
@app.route('/Templates/index.html')
def home():
    user = session.get('user')
    return render_template('index.html', user=user)

@app.route('/login')
@app.route('/login.html')
@app.route('/Templates/login.html')
def login():
    return render_template('login.html')

@app.route('/auth/register', methods=['POST'])
def auth_register():
    role = request.form.get('role', 'student')
    fullname = request.form.get('fullname', '').strip()
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')

    if not username or not email or not password:
        return redirect('/login.html?mode=signup&error=missing_fields')

    hashed_pw = generate_password_hash(password)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (role, fullname, username, email, password) VALUES (?, ?, ?, ?, ?)',
            (role, fullname, username, email, hashed_pw)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.rollback()
        return redirect('/login.html?mode=signup&error=already_exists')
    finally:
        conn.close()

    session.permanent = True
    session['user'] = {'username': username, 'email': email, 'role': role, 'fullname': fullname}

    if role == 'govt':
        return redirect(url_for('dashboard'))
    elif role == 'employer':
        return redirect(url_for('employment'))
    return redirect(url_for('skillgaps'))

@app.route('/auth/login', methods=['POST'])
def auth_login():
    role = request.form.get('role', 'student')
    identifier = request.form.get('identifier', '').strip()
    password = request.form.get('password', '')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE (username = ? OR email = ?) AND role = ?',
        (identifier, identifier, role)
    )
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password'], password):
        session.permanent = True
        session['user'] = {'username': user['username'], 'email': user['email'], 'role': user['role']}
        if role == 'govt':
            return redirect(url_for('dashboard'))
        elif role == 'employer':
            return redirect(url_for('employment'))
        return redirect(url_for('skillgaps'))

    return redirect('/login.html?error=invalid_credentials')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@app.route('/Dashboard.html')
def dashboard():
    return send_from_directory('.', 'Dashboard.html')

@app.route('/workforce')
@app.route('/workforce.html')
def workforce():
    return send_from_directory('.', 'workforce.html')

@app.route('/skillgaps')
@app.route('/skillgaps.html')
def skillgaps():
    return send_from_directory('.', 'skillgaps.html')

@app.route('/employment')
@app.route('/Employement.html')
def employment():
    return send_from_directory('.', 'Employement.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)