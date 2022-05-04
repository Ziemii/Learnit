from tkinter import SE
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
import os
from dotenv import load_dotenv
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from helpers import login_required
import mail_service


load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16) # to change


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# print(os.getenv('BABA'))
# conn = sqlite3.connect('database/learn!t.db')
# cur = conn.cursor();
_DB = os.getenv('DB')
active = [0,0,0]

@app.route('/', methods=['GET', 'POST'])
def index():
    active = [1,0,0]
    return render_template("index.html", active=active)

@app.route('/learning-paths', methods=['GET', 'POST'])
def learningPaths():
    active = [0,1,0]
    return render_template("learning-paths.html", active=active)

@app.route('/about', methods=['GET', 'POST'])
@login_required
def about():
    if(request.method=='GET'):
        active = [0,0,1]
        return render_template("about.html", active=active)

@app.route('/login', methods=['GET', 'POST'])
def login():
    active = [0,0,0]
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userId = None
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor();
            user = cur.execute("SELECT passwordhash, id, isActive FROM users WHERE login = ?", (username,)).fetchall()
            if not user:
                return render_template('login.html', active=active, userError = 'Username not found.')
            if not check_password_hash(user[0][0], password):
                return render_template('login.html', active=active, passwordError = 'Incorrect password.')
            if user[0][2] != 1:
                return render_template('login.html', active=active, passwordError = 'Account inactive, check your email.')
            userId=user[0][1]
        session['user_id'] = userId
        
        return redirect("/")

    else:
        
        
        return render_template("login.html", active=active)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor();
            user = cur.execute("SELECT * FROM users WHERE login = ?", (username,)).fetchall()
            dbemail = cur.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            if not dbemail and not user:
                hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                cur.execute("INSERT INTO users (login, passwordhash, email, isActive) VALUES (?,?,?,?)",(str(username),str(hash),str(email), 0))
                userId = cur.execute("SELECT id FROM users WHERE login = ?", (username,)).fetchall()[0][0]
                verification = str(generate_password_hash(username, method='pbkdf2:sha256', salt_length=8))
                # veritest = verification.lstrip("pbkdf2:sha256:260000")
                cur.execute("INSERT INTO verifications (verification, userId) VALUES (?,?)",(verification,userId))
                mail_service.SendConfirmation(email, verification.lstrip("pbkdf2:sha256:260000"))
                return render_template('register_success.html', active=active)
            if not dbemail:
                return render_template('register.html', active=active, userError = 'Username already in use')
            else:
                return render_template('register.html', active=active, emailError = 'E-mail already in use')
            
            
        
        
        return redirect("/")

        return render_template("register.html", active=active)
    else:
        return render_template("register.html", active=active)


@app.route('/privacy', methods=['GET'])
def terms():
    return render_template('privacy.html', active=active)

@app.route('/confirmation', methods=['GET'])
def confirmation():
    hashParam = request.args.get('pass')
    with sqlite3.connect(_DB) as conn:
        cur = conn.cursor();
        cur.execute("UPDATE users SET isActive = 1 FROM (SELECT userId from verifications WHERE verification = ?) as verifications WHERE users.id = verifications.userId;",(str('pbkdf2:sha256:260000'+hashParam),))
    return render_template('login.html', active=active, accActive='Account activated.')