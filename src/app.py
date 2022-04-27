from flask import Flask, render_template, request

app = Flask(__name__)

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

    active = [0,1,0]
    return render_template("login.html", active=active)



@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template("register.html", active=active)