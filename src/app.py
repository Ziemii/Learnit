from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

app = Flask(__name__)


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
def about():
    if(request.method=='GET'):
        active = [0,0,1]
        return render_template("about.html", active=active)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor();
            user = cur.execute("SELECT login FROM users WHERE login = ?", (request.form.get('username'),)).fetchall()
            print(user)
            if not user:
               return redirect('/')
            return redirect('/')
        
    else:
        active = [0,0,0]
        return render_template("login.html", active=active)



@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html", active=active)