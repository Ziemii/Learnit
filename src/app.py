# from crypt import methods
# from tkinter import SE
#from crypt import methods

from msilib.schema import Error
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
import json
from flask import Response


load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  # to change


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

_DB = os.getenv('DB')
active = [0, 0, 0]

# Landing page


@app.route('/', methods=['GET', 'POST'])
def index():
    active = [1, 0, 0]
    return render_template("index.html", active=active)

#


@app.route('/learning-paths', methods=['GET'])
def learningPaths():
    active = [0, 1, 0]
    tag = request.args.get('tag')
    page = request.args.get('page')
    if page:
        page = int(page)
    search = request.args.get('search')

    if not page:
        page = 1

    sortBy = request.args.get('sortBy')  # rating, alpha

    limit = 6
    with sqlite3.connect(_DB) as conn:
        cur = conn.cursor()

        count = int(cur.execute(
            "SELECT COUNT(*) FROM lpaths;").fetchall()[0][0])

        pages = 0
        if((count % limit) > 0):
            pages = int(count/limit)+1
        else:
            pages = int(count/limit)

        if(tag):

            lpaths = cur.execute(
                "SELECT * FROM lpaths WHERE tags LIKE ?;", ("%"+tag+"%",)).fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, pages=0, tag=tag)

        if(search):
            lpaths = cur.execute(
                "SELECT * FROM lpaths WHERE title LIKE ? ORDER BY id DESC LIMIT ?;", ("%"+search+"%", limit,)).fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, tag='x')

        if(sortBy and page):

            match sortBy:
                case 'rating':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY rating DESC LIMIT ? OFFSET ?;", (limit, (page-1)*limit)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case 'alpha':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY title LIMIT ? OFFSET ?;", (limit, (page-1)*limit)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!rating':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY rating LIMIT ? OFFSET ?;", (limit, (page-1)*limit)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!alpha':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY title DESC LIMIT ? OFFSET ?;", (limit, (page-1)*limit)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
        if(sortBy):
            match sortBy:
                case 'rating':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY rating LIMIT ?;", (limit,)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case 'alpha':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY title LIMIT ?;", (limit,)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!rating':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY rating DESC LIMIT ?;", (limit,)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!alpha':
                    lpaths = cur.execute(
                        "SELECT * FROM lpaths ORDER BY title DESC LIMIT ?;", (limit,)).fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
        if(page):

            lpaths = cur.execute(
                "SELECT * FROM lpaths ORDER BY id DESC LIMIT ? OFFSET ?;", (limit, (page-1)*limit)).fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages)

        lpaths = cur.execute(
            "SELECT * FROM lpaths ORDER BY id DESC LIMIT ?;", (limit,)).fetchall()

        if not lpaths:
            active = [0, 0, 0]
            return render_template('errorpage.html', active=active)

    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages)


@app.route('/about', methods=['GET', 'POST'])
def about():
    if(request.method == 'GET'):
        active = [0, 0, 1]
        return render_template("about.html", active=active)


@app.route('/login', methods=['GET', 'POST'])
def login():
    active = [0, 0, 0]
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userId = None
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor()
            user = cur.execute(
                "SELECT passwordhash, id, isActive FROM users WHERE login = ?", (username,)).fetchall()
            if not user:
                return render_template('login.html', active=active, userError='Username not found.')
            if not check_password_hash(user[0][0], password):
                return render_template('login.html', active=active, passwordError='Incorrect password.')
            if user[0][2] != 1:
                return render_template('login.html', active=active, passwordError='Account inactive, check your email.')
            userId = user[0][1]
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
            cur = conn.cursor()
            user = cur.execute(
                "SELECT * FROM users WHERE login = ?", (username,)).fetchall()
            dbemail = cur.execute(
                "SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            if not dbemail and not user:
                hash = generate_password_hash(
                    password, method='pbkdf2:sha256', salt_length=8)
                cur.execute("INSERT INTO users (login, passwordhash, email, isActive) VALUES (?,?,?,?)", (str(
                    username), str(hash), str(email), 0))
                userId = cur.execute(
                    "SELECT id FROM users WHERE login = ?", (username,)).fetchall()[0][0]
                verification = str(generate_password_hash(
                    username, method='pbkdf2:sha256', salt_length=8))
                # veritest = verification.lstrip("pbkdf2:sha256:260000")
                cur.execute(
                    "INSERT INTO verifications (verification, userId) VALUES (?,?)", (verification, userId))
                mail_service.SendConfirmation(
                    email, verification.lstrip("pbkdf2:sha256:260000"))
                return render_template('register_success.html', active=active)
            if not dbemail:
                return render_template('register.html', active=active, userError='Username already in use')
            else:
                return render_template('register.html', active=active, emailError='E-mail already in use')

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
        cur = conn.cursor()
        cur.execute("UPDATE users SET isActive = 1 FROM (SELECT userId from verifications WHERE verification = ?) as verifications WHERE users.id = verifications.userId;", (str(
            'pbkdf2:sha256:260000'+hashParam),))
        cur.execute("DELETE from verifications WHERE verification = ?;", (str('pbkdf2:sha256:260000'+hashParam),))
        return render_template('login.html', active=active, accActive='Account activated.')
    return render_template('errorpage.html', active=active)

@app.route('/new', methods=['GET', 'POST'])
@login_required
def newPath():
    active = [0, 0, 0]

    if request.method == 'POST':
        title = request.form.get('title')
        tags = request.form.get('tags')
        excerpt = request.form.get('excerpt')
        body = request.form.get('body')
        filteredTags = ''.join(
            (filter(lambda x: x not in [' ', ',', '!', '?'], tags)))
        userId = session['user_id']
        print(f"Title: {title}")
        print(f"body: {body}")
        print(f"Tags: {tags}")
        print(f"filtered tags: {filteredTags}")
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO lpaths (title, tags, excerpt, body, userId) VALUES (?,?,?,?,?)",
                        (title, filteredTags, excerpt, body, userId))

        return redirect("/new")

    else:

        return render_template("new_path.html", active=active)


@app.route('/recover', methods=['GET', 'POST'])
@login_required
def recover():
    if request.method == 'POST':
        
        email = request.form.get('email')
        success = None
        hash = None
        print(f"email: {email}")
        try:
            with sqlite3.connect(_DB) as conn:
                cur = conn.cursor();
                userId = cur.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchall()[0][0]
                if not userId:
                    return render_template('recover.html', active=active, error = 'Email not in database')
                recovery = str(generate_password_hash(
                    email, method='pbkdf2:sha256', salt_length=8))
                conn.execute("INSERT INTO recoveries (recovery, userId) VALUES (?,?)", (recovery, userId))
                mail_service.SendRecovery(email, hash)
        except Exception as error:
            print(error)
            return render_template("errorpage.html", error="Error occured")

        return render_template("recover.html", active=active, success=success)
    else:
        return render_template("recover.html", active=active)


@app.route('/path', methods=['GET'])
def path():
    pathId = request.args.get('id')
    lpath = None
    bookmark = 0
    userId = None
    voted = None
    # if(session['user_id']):
    userId = session.get('user_id')
    # print(f"userId {userId}")
    with sqlite3.connect(_DB) as conn:
        cur = conn.cursor()
        if(userId != None):
            voted = cur.execute(
                "SELECT voted FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0][0]
            bookmarks = cur.execute(
                "SELECT bookmarks FROM users WHERE id = ?", (userId,)).fetchall()[0][0]
            # print(f"voted {voted}")
            bookmarksList = bookmarks.split(',')
            print(f"bookmarksList: {bookmarksList}")
            votedList = voted.split(',')
            # print(f"votedList {votedList}")
            if(str(userId) in votedList):
                voted = 'voted'
            if(str(pathId) in bookmarksList):
                bookmark = 1
        lpath = cur.execute(
            "SELECT * FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0]
        if not lpath:
            return redirect('/')
        # print(lpath)

    return render_template("path.html", active=active, lpath=lpath, userId=userId, voted=voted, bookmark=bookmark)


@app.route('/rate', methods=['POST'])
@login_required
def rate():
    pathId = request.form.get('pathId')
    userId = request.form.get('userId')
    with sqlite3.connect(_DB) as conn:
        if(userId != None and pathId != None):
            cur = conn.cursor()
            voted = cur.execute(
                "SELECT voted FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0][0]
            rating = cur.execute(
                "SELECT rating FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0][0]

            cur.execute("UPDATE lpaths SET rating = ? WHERE id = ?",
                        (rating+1, pathId))
            cur.execute("UPDATE lpaths SET voted = ? WHERE id = ?",
                        (voted+","+userId, pathId))

            voted = cur.execute(
                "SELECT voted FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0][0]
            print(voted)
            if(userId in voted):
                userId = 'voted'
            lpath = cur.execute(
                "SELECT * FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0]
            if not lpath:
                return redirect('/')
            # print(lpath)
            return Response("RATED", status=201, mimetype='application/json')
        return Response("NOT RATED", status=400, mimetype='application/json')


@app.route('/bookmark', methods=['POST'])
@login_required
def bookmark():
    pathId = request.form.get('pathId')
    userId = request.form.get('userId')
    with sqlite3.connect(_DB) as conn:
        if(userId != None and pathId != None):
            cur = conn.cursor()
            bookmarks = cur.execute(
                "SELECT bookmarks FROM users WHERE id = ?", (int(userId),)).fetchall()[0][0]
            bookmarks = bookmarks.split(',')

            if(pathId in bookmarks):
                bookmarks.remove(str(pathId))
                bookmarks = ",".join(bookmarks)
                cur.execute(
                    "UPDATE users SET bookmarks = ? WHERE id = ?", (bookmarks, userId))

            else:
                bookmarks.append(pathId)
                bookmarks = ",".join(bookmarks)
                cur.execute(
                    "UPDATE users SET bookmarks = ? WHERE id = ?", (bookmarks, userId))

            return Response("BOOKMARKING DONE", status=201, mimetype='application/json')
        return Response("BOOKMARKING FAILED", status=400, mimetype='application/json')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    userId = session['user_id']
    bookmarks = []
    if(userId):
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor()
            user = cur.execute(
                "SELECT * FROM users WHERE id = ?", (int(userId),)).fetchall()[0]
            bookmarksId = cur.execute(
                "SELECT bookmarks FROM users WHERE id = ?", (int(userId),)).fetchall()[0][0]
            print(f"user: {user}")
            bookmarksId = bookmarksId.split(',')
            for pathId in bookmarksId:
                bookmarks.append(cur.execute(
                    "SELECT * FROM lpaths WHERE id = ?", (int(pathId),)).fetchall())
            bookmarks.pop(0)

            submissions = cur.execute(
                "SELECT * FROM lpaths WHERE userId = ?", (int(userId),)).fetchall()
    return render_template('account.html', active=active, bookmarks=bookmarks, submissions=submissions, userId=userId, user=user)


@app.route('/delete', methods=['POST'])
@login_required
def delete():

    pathId = request.form.get('pathId')
    with sqlite3.connect(_DB) as conn:
        if(pathId != None):
            cur = conn.cursor()
            cur.execute("DELETE FROM lpaths WHERE id=? ;", (int(pathId),))
            return Response("DELETE DONE", status=201, mimetype='application/json')
        return Response("DELETE FAILED", status=400, mimetype='application/json')


@app.route('/deleteAccount', methods=['POST'])
@login_required
def deleteAccount():

    userId = request.get_json()
    print(f"userId: {userId}")
    with sqlite3.connect(_DB) as conn:
        if(userId != None):
            print("not none")
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=? ;", (int(userId),))
            cur.execute("DELETE FROM lpaths WHERE userId=? ;", (int(userId),))
            return Response("DELETE DONE", status=201, mimetype='application/json')
        return Response("DELETE FAILED", status=400, mimetype='application/json')

@app.route('/controlpanel', methods=['GET', 'POST'])
def controlPanel():
    active = [0, 0, 0]
    # session.clear()
    session['admin_id'] = None
    if request.method == 'POST':
        password = request.form.get('password')
        adminId = None
        with sqlite3.connect(_DB) as conn:
            cur = conn.cursor()
            password = cur.execute(
                "SELECT password FROM admin WHERE id = 1").fetchall()[0][0]
            print(f"password {password}")
            if not password:
                return redirect('/')
            if password != password:
                return redirect('/')
            adminId = 1
        session['admin_id'] = adminId

        return redirect("/controlpanel")
    if request.method == 'GET' and session['admin_id'] != None:
        return render_template("controlpanel.html", active=active, admin=1)
    else:
        return render_template("controlpanel.html", active=active)

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    active = [0,0,0] 
    if request.method == 'POST':
        userId = session['user_id']
        old = request.form.get('old')
        password = request.form.get('password')
        try:
            with sqlite3.connect(_DB) as conn:
                cur = conn.cursor()
                passwordHash = cur.execute(
                    "SELECT passwordhash FROM users WHERE id = ?", (int(userId),)).fetchall()[0][0]
                print(f"password hash: {passwordHash}")
                if passwordHash != None:
                    hash = generate_password_hash(
                        old, method='pbkdf2:sha256', salt_length=8)
                    print(f"hash: {hash}")
                    if check_password_hash(passwordHash, old):
                        newHash = hash = generate_password_hash(
                        password, method='pbkdf2:sha256', salt_length=8)
                        cur.execute("UPDATE users SET passwordhash = ?;",(newHash,))
                        return render_template("changepassword.html", active=active, passwordChange="Password changed")
                    return render_template("changepassword.html", active=active, passwordError="Incorrect password")
                else:
                    return render_template("changepassword.html", active=active, passwordChange="Password not changed")
        except Exception as error:
            return print(f"error: {error}")
    else:
        return render_template("changepassword.html", active=active)