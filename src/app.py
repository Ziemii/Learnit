
### Main flask application ###

# Import section
from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
import os
from dotenv import load_dotenv
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from helpers import login_required, admin_required
import mail_service
from flask import Response

# Loads .env file
load_dotenv() 

# Flask app initialization
app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

# Flask session configuration and initialization
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Database address
DB = os.getenv('DB')

# Initial state for active nav link
active = [0, 0, 0]

# Landing page
@app.route('/', methods=['GET'])
def index():
    return redirect('/learning-paths')

# Learning paths list route with sorting functionality and pagination
# Sorting solution implemented as SQL queries requesting already sorted results
@app.route('/learning-paths', methods=['GET'])
def learningPaths():
    # Sets learning paths nav link active
    active = [0, 1, 0]

    # Reads GET request arguments
    tag = request.args.get('tag')
    page = request.args.get('page')
    search = request.args.get('search')
    sortBy = request.args.get('sortBy')

    # If there was page argument provided, convert it to integer, else first page will be shown     
    if page:
        page = int(page)
    if not page:
        page = 1

    # Limits number of learning paths shown on single page
    limit = 6

    # Connects to learning paths table in database     
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()

        # Counts how many active submissions there are and calculates number of pages needed
        count = int(cur.execute(
            "SELECT COUNT(*) FROM lpaths WHERE isActive=1;").fetchall()[0][0])
        pages = 0
        if((count % limit) > 0):
            pages = int(count/limit)+1
        else:
            pages = int(count/limit)

        # Depending on GET request composition returns requested results
        # Results filtered by tag
        if(tag):
            lpaths = cur.execute(
                "SELECT * FROM lpaths WHERE tags LIKE ? AND isActive = 1;", ("%"+tag+"%",)).fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, pages=0, tag=tag)
        
        # Results filtered by searched title
        if(search):
            lpaths = cur.execute(
                "SELECT * FROM lpaths WHERE title LIKE ? AND isActive = 1 ORDER BY id DESC LIMIT ?;", ("%"+search+"%", limit,)).fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, tag='x')
        
        
        # Sorted results
        if(sortBy):

            if(sortBy[0] == "!"):
                order = "DESC"
                if(sortBy[1] == "a"):
                    orderBy = "title"
                else:
                    orderBy = "rating"
            else:
                order = "ASC"
                if(sortBy[0] == "a"):
                    orderBy = "title"
                else:
                    orderBy = "rating"
            
            # Construct database query for sorted and paged results depending on GET request parameters
            lpaths = cur.execute(f"SELECT * FROM lpaths WHERE isActive=1 ORDER BY {orderBy} {order} LIMIT ? OFFSET ?;", (limit, (page-1)*limit if page else "0")).fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)

        
        # Default paging and sorting
        lpaths = cur.execute(
            "SELECT * FROM lpaths WHERE isActive=1 ORDER BY id DESC LIMIT ?;", (limit,)).fetchall()
        
        # Shows error page if learning paths couldn't be acquired
        if not lpaths:
            active = [0, 0, 0]
            return render_template('errorpage.html', active=active)

    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages)

# About route
@app.route('/about', methods=['GET'])
def about():
    if(request.method == 'GET'):
        active = [0, 0, 1]
        return render_template("about.html", active=active)

# Login functionality implementation
@app.route('/login', methods=['GET', 'POST'])
def login():
    active = [0, 0, 0]

    # Clears sessions, if any
    session.clear()

    
    # Default behaviour is when GET method asks for login form, 
    # POST method triggers login action itself     
    
    # Check if request method is POST, else render login.html
    if request.method == 'POST':
        
        # Reads form inputs
        username = request.form.get('username')
        password = request.form.get('password')
        userId = None
        
        # Connects to database and checks if there is user as provided in form, 
        # if password hash saved for this user checks with password provided in form
        # and if account is active. If all is valid, user's id is saved within session and user is logged in.
        with sqlite3.connect(DB) as conn:
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

#Logout functionality
@app.route('/logout', methods=['GET'])
def logout():
    # Clears session and redirects to root page
    session.clear()
    return redirect('/')


# Register functionality implementation #
# Similar to login, default behaviour is when GET method asks for register form, 
# POST method triggers registration action itself     

# Check if request method is POST, else render register.html
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        # Read from form input fields
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        # Connects to database, checks if there is user or e-mail already in database
        # if not, generates new password hash, saves credentials to database and sends activation link
        # to provided e-mail 
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            user = cur.execute(
                "SELECT * FROM users WHERE login = ?", (username,)).fetchall()
            dbemail = cur.execute(
                "SELECT * FROM users WHERE email = ?", (email,)).fetchall()
            if not dbemail and not user:
                hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                cur.execute("INSERT INTO users (login, passwordhash, email, isActive) VALUES (?,?,?,?)", (str(username), str(hash), str(email), 0))
                userId = cur.execute("SELECT id FROM users WHERE login = ?", (username,)).fetchall()[0][0]
                verification = str(generate_password_hash(username, method='pbkdf2:sha256', salt_length=8))
                cur.execute( "INSERT INTO verifications (verification, userId) VALUES (?,?)", (verification, userId))
                mail_service.SendConfirmation(
                    email, verification.lstrip("pbkdf2:sha256:260000"))
                return render_template('register_success.html', active=active)
            if not dbemail:
                return render_template('register.html', active=active, userError='Username already in use')
            else:
                return render_template('register.html', active=active, emailError='E-mail already in use')
        return redirect("/")
    else:
        return render_template("register.html", active=active)

# Privacy policy page
@app.route('/privacy', methods=['GET'])
def terms():
    return render_template('privacy.html', active=active)

# Account activation API route #
# activation link contains verification hash code as parameter
# if verification hash code matches any verifications table column row in database
# user account referenced in that row becomes active and row is deleted.
@app.route('/confirmation', methods=['GET'])
def confirmation():
    hashParam = request.args.get('pass')
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET isActive = 1 FROM (SELECT userId from verifications WHERE verification = ?) as verifications WHERE users.id = verifications.userId;", (str(
            'pbkdf2:sha256:260000'+hashParam),))
        cur.execute("DELETE from verifications WHERE verification = ?;",(str('pbkdf2:sha256:260000'+hashParam),))
        return render_template('login.html', active=active, accActive='Account activated.')
    return render_template('errorpage.html', active=active)

# New sumbission creating route #
# When request method is GET renders form page with integrated text editor,
# else saves submission in database as inactive
@app.route('/new', methods=['GET', 'POST'])
@login_required
def newPath():
    active = [0, 0, 0]

    if request.method == 'POST':
        
        # Reads form arguments
        title = request.form.get('title')
        tags = request.form.get('tags')
        excerpt = request.form.get('excerpt')
        body = request.form.get('body')
        
        # Filters tags string from unwanted characters
        filteredTags = ''.join(
            (filter(lambda x: x not in [' ', ',', '!', '?'], tags)))
        
        # Reads user id from session for sumbission saving purpose
        userId = session['user_id']
        
        # Tries connection to database to save submission
        # renders error page if exception raised.
        try:
            with sqlite3.connect(DB) as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO lpaths (title, tags, excerpt, body, userId) VALUES (?,?,?,?,?)",(title, filteredTags, excerpt, body, userId))
        except Exception:
            return render_template("errorpage.html", error="Database error, please try again.")

        return render_template("new_path.html", active=active, success=1)
    else:
        return render_template("new_path.html", active=active)

# Password recovery route #
# Makes distinction between couple POST requests types
# If POST contain email address API sends password reset link
# else POST request must be from new password form 
# which is reached by opening recovery link
# GET request renders e-mail input form
@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        if(request.form.get('email', False)):
            email = request.form.get('email')
            try:
                with sqlite3.connect(DB) as conn:
                    cur = conn.cursor()
                    userId = cur.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchall()[0][0]
                    if not userId:
                        return render_template('recover.html', active=active, error='Email not in database')
                    # Generates recover hash code
                    recovery = str(generate_password_hash( email, method='pbkdf2:sha256', salt_length=8))
                    # Saves recover hash code in database
                    conn.execute("INSERT INTO recoveries (recovery, userId) VALUES (?,?)", (recovery, userId))
                    mail_service.SendRecovery(email, recovery)
            except Exception as error:
                print(error)
                return render_template("errorpage.html", active=active, error="Error occured")

            return render_template("recover.html", active=active, success="Request accepted, check your mail.")
        else:
            # Reads form input fields
            userId = request.form.get('formId')
            password = request.form.get('password')
            try:
                with sqlite3.connect(DB) as conn:
                    cur = conn.cursor()
                    # Generates new hash code from provided password and saves it in database
                    hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)
                    cur.execute("UPDATE users SET passwordhash = ? WHERE id = ?;", (hash, userId))
                    return render_template("recover.html", active=active, success="Password changed")

            except Exception as error:
                return print(f"error: {error}")

    else:
        recovery = request.args.get('pass', None)
        if recovery != None:
            try:
                with sqlite3.connect(DB) as conn:
                    cur = conn.cursor()
                    dbRecovery = cur.execute( "SELECT COUNT(recovery) FROM recoveries WHERE recovery LIKE ?;", (recovery,)).fetchall()[0][0]
                    if int(dbRecovery) != 1:
                        return render_template('recover.html', active=active, error='Error occurred, please contact owner.')
                    else:
                        formId = cur.execute("SELECT users.id FROM users JOIN recoveries ON recoveries.userId = users.id WHERE recovery = ?;", (recovery,)).fetchall()[0][0]
                        cur.execute("DELETE from recoveries WHERE recovery = ?;", (recovery,))
                        return render_template("recover.html", active=active, form=formId)
            except Exception as error:
                print(f"Exception: {error}")
                return render_template("errorpage.html", active=active, error="Error occured")

    return render_template("recover.html", active=active)

# Path presentation route #
# Fetches learning path data from database using id
# and renders particular path page
@app.route('/path', methods=['GET'])
def path():
    pathId = request.args.get('id')
    lpath = None
    bookmark = 0
    userId = None
    voted = None
    userId = session.get('user_id')
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        if(userId != None):
            voted = cur.execute(
                "SELECT voted FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0][0]
            bookmarks = cur.execute(
                "SELECT bookmarks FROM users WHERE id = ?", (userId,)).fetchall()[0][0]
            bookmarksList = bookmarks.split(',')
            votedList = voted.split(',')
            if(str(userId) in votedList):
                voted = 'voted'
            if(str(pathId) in bookmarksList):
                bookmark = 1
        lpath = cur.execute(
            "SELECT * FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0]
        if not lpath:
            # Redirects to app root if there is no path with requested id
            return redirect('/')

    return render_template("path.html", active=active, lpath=lpath, userId=userId, voted=voted, bookmark=bookmark)

# Rating endpoint #
# Updates endorsements count adding 1 and saves which users already voted
@app.route('/rate', methods=['POST'])
@login_required
def rate():
    pathId = request.form.get('pathId')
    userId = str(session['user_id'])
    with sqlite3.connect(DB) as conn:
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
            if(userId in voted):
                userId = 'voted'
            lpath = cur.execute(
                "SELECT * FROM lpaths WHERE id = ?", (pathId,)).fetchall()[0]
            if not lpath:
                return redirect('/')
            return Response("RATED", status=201, mimetype='application/json')
        return Response("NOT RATED", status=400, mimetype='application/json')

# Bookmarking endpoint #
# Adds to or deletes from account bookmarks tab
@app.route('/bookmark', methods=['POST'])
@login_required
def bookmark():
    pathId = request.form.get('pathId')
    userId = session['user_id']    
    with sqlite3.connect(DB) as conn:
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

            return Response("BOOKMARKING DONE", status=200, mimetype='application/json')
        return Response("BOOKMARKING FAILED", status=400, mimetype='application/json')

# Account page # 
# Fetches database for user bookmars, submissions and account information 
# then renders account page
@app.route('/account', methods=['GET'])
@login_required
def account():
    userId = session['user_id']
    bookmarks = []
    if(userId):
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            user = cur.execute(
                "SELECT * FROM users WHERE id = ?", (int(userId),)).fetchall()[0]
            bookmarksId = cur.execute(
                "SELECT bookmarks FROM users WHERE id = ?", (int(userId),)).fetchall()[0][0]
            bookmarksId = bookmarksId.split(',')
            for pathId in bookmarksId:
                bookmark = cur.execute(
                    "SELECT * FROM lpaths WHERE id = ?", (int(pathId),)).fetchall()
                print(f"bookmark {bookmark} ")
                if(bookmark != []):
                    bookmarks.append(bookmark)
            submissions = cur.execute(
                "SELECT * FROM lpaths WHERE userId = ?;", (int(userId),)).fetchall()
    return render_template('account.html', active=active, bookmarks=bookmarks, submissions=submissions, userId=userId, user=user)

# Submission deletion #
# Endpoint for submission deletion
# Submission id is supplied with POST request and then row containing that id is removed from table
@app.route('/delete', methods=['POST'])
@login_required
def delete():
    pathId = request.form.get('pathId')
    with sqlite3.connect(DB) as conn:
        if(pathId != None):
            cur = conn.cursor()
            cur.execute("DELETE FROM lpaths WHERE id=? ;", (int(pathId),))
            return Response("DELETE DONE", status=200, mimetype='application/json')
        return Response("DELETE FAILED", status=400, mimetype='application/json')

# Account deletion endpoint #
# Accepts request to delete account
# Deletes all submissions created on this account
@app.route('/deleteAccount', methods=['POST'])
@login_required
def deleteAccount():

    userId = request.get_json()
    with sqlite3.connect(DB) as conn:
        if(userId != None):
            cur = conn.cursor()
            cur.execute("DELETE FROM lpaths WHERE userId=? ;", (int(userId),))
            cur.execute("DELETE FROM users WHERE id=? ;", (int(userId),))
            redirect('/')
            return Response("DELETE DONE", status=200, mimetype='application/json')
        return Response("DELETE FAILED", status=400, mimetype='application/json')


# Changing password #
# Password change service implementation
# on GET request renders password change form
# on form submission connects to database and compares password hash with provided account password
# if both match generates new password hash from password provided in form and saves it in database
@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    active = [0, 0, 0]
    if request.method == 'POST':
        userId = session['user_id']
        old = request.form.get('old')
        password = request.form.get('password')
        try:
            with sqlite3.connect(DB) as conn:
                cur = conn.cursor()
                passwordHash = cur.execute(
                    "SELECT passwordhash FROM users WHERE id = ?", (int(userId),)).fetchall()[0][0]
                if passwordHash != None:
                    if check_password_hash(passwordHash, old):
                        newHash = generate_password_hash(
                            password, method='pbkdf2:sha256', salt_length=8)
                        cur.execute(
                            "UPDATE users SET passwordhash = ? WHERE id = ?;", (newHash, userId))
                        return render_template("changepassword.html", active=active, passwordChange="Password changed")
                    return render_template("changepassword.html", active=active, passwordError="Incorrect password")
                else:
                    return render_template("changepassword.html", active=active, passwordChange="Password not changed")
        except Exception as error:
            return print(f"error: {error}")
    else:
        return render_template("changepassword.html", active=active)


# Submissions control panel #
# on GET request renders login screen with single input
# after logging in renders list of inactive submissions

@app.route('/controlpanel', methods=['GET', 'POST'])
def controlPanel():
    active = [0, 0, 0]
    if request.method == 'POST':
        password = request.form.get('password')
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            password = cur.execute(
                "SELECT password FROM admin WHERE id = 1").fetchall()[0][0]
            if not password:
                return redirect('/')
            if password != password:
                return redirect('/')
            session['admin_id'] = 1
            evals = cur.execute(
                "SELECT * FROM lpaths WHERE isActive = 0").fetchall()
            if not evals:
                evals = None


        return render_template("controlpanel.html", active=active, admin=1, evals=evals)
    else:

        return render_template("controlpanel.html", active=active)


# Submission activation or rejection #
# complementary endpoint for accepting or rejecting submission
# buttons in control panel triggers POST request with positive or negative decision
# if positive, submission is activated and can be seen on learning paths page
# if negative, submission is deleted from database 
@app.route('/verdict', methods=['POST'])
@admin_required
def verdict():
    id = request.form.get('pathId')
    verdict = str(request.form.get('verdict'))
    try:
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            if (verdict == '1'):
                cur.execute(
                    "UPDATE lpaths SET isActive = 1 WHERE id = ?;", (id,))
            else:
                cur.execute("DELETE FROM lpaths WHERE id = ?;", (id,))
    except Exception as error:
        return print(f"error: {error}")
    return Response("Verdict made", status=200, mimetype='application/json')
