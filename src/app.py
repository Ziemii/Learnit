
from xml.etree.ElementTree import tostring
from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
import os
from dotenv import load_dotenv
import sqlite3
import psycopg2
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from helpers import login_required
import mail_service
from flask import Response


load_dotenv()


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)  # to change


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

_DB = os.getenv('DB')
active = [0, 0, 0]

# host = "ec2-63-32-248-14.eu-west-1.compute.amazonaws.com"
# database = "d9ms06rcrqnfvf"
# user = "dddbjfjmtwvhub"
# password = "0a9c69e2029fbd2be850060af2d063714ef8b423400a1139b3551e3f05ac70ca"
# port = "5432"

# databaseCreds = "host="+host+",database="+database+",user=" + os.environ['DB_USERNAME']+ ",password=" + os.environ['DB_PASSWORD'] 
# databaseCreds = "host="+host+" dbname="+database+" user=" + user+ " password=" + password + " port=" + port
DATABASE_URL = "postgres://dddbjfjmtwvhub:0a9c69e2029fbd2be850060af2d063714ef8b423400a1139b3551e3f05ac70ca@ec2-63-32-248-14.eu-west-1.compute.amazonaws.com:5432/d9ms06rcrqnfvf"


# with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
#     cur = conn.cursor()

#     cur.execute("select * from users")
#     users = cur.fetchall()[0][0]
#     print(f"users {users}")




# Landing page


@app.route('/', methods=['GET'])
def index():
    # active = [0, 1, 0]
    return redirect('/learning-paths')


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

    sortBy = request.args.get('sortBy')

    limit = 6
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM lpaths WHERE isActive=1;")
        count = cur.fetchall()[0][0]
        if (count) == None:
            count = 0
            # return render_template("learning-paths.html", active=active, paths=None, pages=0)
        else:
            count = int(count)
        

        # if():
        #     count = int(cur.execute(
        #         "SELECT COUNT(*) FROM lpaths WHERE isActive=1;").fetchall()[0][0])
        # else:
        #     count = 0

        pages = 0
        if((count % limit) > 0):
            pages = int(count/limit)+1
        else:
            pages = int(count/limit)

        if(tag):
            cur.execute("SELECT * FROM lpaths WHERE tags LIKE %s AND isActive = 1;", ("%"+tag+"%",))
            lpaths = cur.fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, pages=0, tag=tag)

        if(search):
            cur.execute("SELECT * FROM lpaths WHERE title LIKE %s AND isActive = 1 ORDER BY id DESC LIMIT %s;", ("%"+search+"%", limit,))
            lpaths = cur.fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, tag='x')

        if(sortBy and page):

            match sortBy:
                case 'rating':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY rating DESC LIMIT %s OFFSET %s;", (limit, (page-1)*limit))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case 'alpha':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY title LIMIT %s OFFSET %s;", (limit, (page-1)*limit))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!rating':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY rating LIMIT %s OFFSET %s;", (limit, (page-1)*limit))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!alpha':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY title DESC LIMIT %s OFFSET %s;", (limit, (page-1)*limit))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
        if(sortBy):
            match sortBy:
                case 'rating':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY rating LIMIT %s;", (limit,))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case 'alpha':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY title LIMIT %s;", (limit,))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!rating':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY rating DESC LIMIT %s;", (limit,))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
                case '!alpha':
                    cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY title DESC LIMIT %s;", (limit,))
                    lpaths = cur.fetchall()
                    return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages, sortBy=sortBy)
        if(page):
            cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY id DESC LIMIT %s OFFSET %s;", (limit, (page-1)*limit))
            lpaths = cur.fetchall()
            return render_template("learning-paths.html", active=active, paths=lpaths, pages=pages)
        
        cur.execute("SELECT * FROM lpaths WHERE isActive=1 ORDER BY id DESC LIMIT %s;", (limit,))
        lpaths = cur.fetchall()

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
        print(f"username sent {username}")
        password = request.form.get('password')
        userId = None
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            cur = conn.cursor()
            cur.execute("SELECT passwordhash, id, isActive FROM users WHERE login = %s", (username,))
            user=cur.fetchall()
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
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            cur = conn.cursor()
            user = cur.execute(
                "SELECT * FROM users WHERE login = %s", (username,)) #.fetchall()
            dbemail = cur.execute(
                "SELECT * FROM users WHERE email = %s", (email,))#.fetchall()
            if not dbemail and not user:
                hash = generate_password_hash(
                    password, method='pbkdf2:sha256', salt_length=8)
                cur.execute("INSERT INTO users (login, passwordhash, email, isActive) VALUES (%s,%s,%s,%s);", (str(
                    username), str(hash), str(email), 0))
                verification = str(generate_password_hash(
                    username, method='pbkdf2:sha256', salt_length=8))
                cur.execute(
                    "INSERT INTO verifications (verification, email) VALUES (%s,%s)", (verification, email))
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
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET isActive = 1 FROM (SELECT email from verifications WHERE verification = %s) as verifications WHERE users.email = verifications.email;", (str(
            'pbkdf2:sha256:260000'+hashParam),))
        cur.execute("DELETE from verifications WHERE verification = %s;",
                    (str('pbkdf2:sha256:260000'+hashParam),))
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
        try:
            with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
                cur = conn.cursor()
                cur.execute("INSERT INTO lpaths (title, tags, excerpt, body, userId) VALUES (%s,%s,%s,%s,%s)",
                            (title, filteredTags, excerpt, body, userId))
        except Exception:
            return render_template("errorpage.html", error="Database error.")

        return render_template("new_path.html", active=active, success=1)

    else:

        return render_template("new_path.html", active=active)


@app.route('/recover', methods=['GET', 'POST'])
def recover():
    if request.method == 'POST':
        if(request.form.get('email', False)):
            email = request.form.get('email')
            success = None
            try:
                with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
                    cur = conn.cursor()
                    userId = cur.execute(
                        "SELECT id FROM users WHERE email = %s", (email,)).fetchall()[0][0]
                    if not userId:
                        return render_template('recover.html', active=active, error='Email not in database')
                    recovery = str(generate_password_hash(
                        email, method='pbkdf2:sha256', salt_length=8))
                    conn.execute(
                        "INSERT INTO recoveries (recovery, userId) VALUES (%s,%s)", (recovery, userId))
                    mail_service.SendRecovery(email, recovery)
            except Exception as error:
                print(error)
                return render_template("errorpage.html", active=active, error="Error occured")

            return render_template("recover.html", active=active, success="Request accepted, check your mail.")
        else:
            userId = request.form.get('formId')
            password = request.form.get('password')
            try:
                with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
                    cur = conn.cursor()

                    hash = generate_password_hash(
                        password, method='pbkdf2:sha256', salt_length=8)

                    cur.execute(
                        "UPDATE users SET passwordhash = %s WHERE id = %s;", (hash, userId))
                    return render_template("recover.html", active=active, success="Password changed")

            except Exception as error:
                return print(f"error: {error}")

    else:
        recovery = request.args.get('pass', None)
        if recovery != None:
            try:
                with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
                    cur = conn.cursor()
                    dbRecovery = cur.execute(
                        "SELECT COUNT(recovery) FROM recoveries WHERE recovery LIKE %s;", (recovery,)).fetchall()[0][0]
                    if int(dbRecovery) != 1:
                        return render_template('recover.html', active=active, error='Error occurred, please contact owner.')
                    else:
                        formId = cur.execute(
                            "SELECT users.id FROM users JOIN recoveries ON recoveries.userId = users.id WHERE recovery = %s;", (recovery,)).fetchall()[0][0]
                        cur.execute(
                            "DELETE from recoveries WHERE recovery = %s;", (recovery,))
                        return render_template("recover.html", active=active, form=formId)
            except Exception as error:
                print(f"Exception: {error}")
                return render_template("errorpage.html", active=active, error="Error occured")

    return render_template("recover.html", active=active)


@app.route('/path', methods=['GET'])
def path():
    pathId = request.args.get('id')
    lpath = None
    bookmark = 0
    userId = None
    voted = None
    userId = session.get('user_id')
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        cur = conn.cursor()
        if(userId != None):
            cur.execute(
                "SELECT voted FROM lpaths WHERE id = %s", (pathId,))
            voted = cur.fetchall()[0][0]
            print(f"voted {voted}")
            cur.execute(
                "SELECT bookmarks FROM users WHERE id = %s", (userId,))
            bookmarks = cur.fetchall()[0][0]
            print(f"bookmarks {bookmarks}")
            bookmarksList = bookmarks.split(',')
            votedList = voted.split(',')
            if(str(userId) in votedList):
                voted = 'voted'
            if(str(pathId) in bookmarksList):
                bookmark = 1
        cur.execute(
            "SELECT * FROM lpaths WHERE id = %s", (pathId,))
        lpath = cur.fetchall()[0]
        if not lpath:
            return redirect('/')

    return render_template("path.html", active=active, lpath=lpath, userId=userId, voted=voted, bookmark=bookmark)


@app.route('/rate', methods=['POST'])
@login_required
def rate():
    pathId = request.form.get('pathId')
    userId = request.form.get('userId')
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        if(userId != None and pathId != None):
            cur = conn.cursor()
            cur.execute("SELECT voted FROM lpaths WHERE id = %s", (pathId,))
            voted = cur.fetchall()[0][0]
            cur.execute("SELECT rating FROM lpaths WHERE id = %s", (pathId,))
            rating = cur.fetchall()[0][0]

            cur.execute("UPDATE lpaths SET rating = %s WHERE id = %s",
                        (rating+1, pathId))
            cur.execute("UPDATE lpaths SET voted = %s WHERE id = %s",
                        (voted+","+userId, pathId))

            cur.execute("SELECT voted FROM lpaths WHERE id = %s", (pathId,))
            voted =cur.fetchall()[0][0]
            if(userId in voted):
                userId = 'voted'
            cur.execute("SELECT * FROM lpaths WHERE id = %s", (pathId,))
            lpath = cur.fetchall()[0]
            if not lpath:
                return redirect('/')
            return Response("RATED", status=201, mimetype='application/json')
        return Response("NOT RATED", status=400, mimetype='application/json')


@app.route('/bookmark', methods=['POST'])
@login_required
def bookmark():
    pathId = request.form.get('pathId')
    userId = request.form.get('userId')
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        if(userId != None and pathId != None):
            cur = conn.cursor()
            cur.execute("SELECT bookmarks FROM users WHERE id = %s", (int(userId),))
            bookmarks = cur.fetchall()[0][0]
            bookmarks = bookmarks.split(',')

            if(pathId in bookmarks):
                bookmarks.remove(str(pathId))
                bookmarks = ",".join(bookmarks)
                cur.execute(
                    "UPDATE users SET bookmarks = %s WHERE id = %s", (bookmarks, userId))

            else:
                bookmarks.append(pathId)
                bookmarks = ",".join(bookmarks)
                cur.execute(
                    "UPDATE users SET bookmarks = %s WHERE id = %s", (bookmarks, userId))

            return Response("BOOKMARKING DONE", status=201, mimetype='application/json')
        return Response("BOOKMARKING FAILED", status=400, mimetype='application/json')


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    userId = session['user_id']
    bookmarks = []
    if(userId):
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM users WHERE id = %s", (int(userId),))
            user = cur.fetchall()[0]
            cur.execute("SELECT bookmarks FROM users WHERE id = %s", (int(userId),))
            bookmarksId = cur.fetchall()[0][0]
            bookmarksId = bookmarksId.split(',')
            for pathId in bookmarksId:
                cur.execute("SELECT * FROM lpaths WHERE id = %s", (int(pathId),))
                bookmarks.append(cur.fetchall())
            bookmarks.pop(0)
            cur.execute(
                "SELECT * FROM lpaths WHERE userId = %s;", (int(userId),))
            submissions = cur.fetchall()
    return render_template('account.html', active=active, bookmarks=bookmarks, submissions=submissions, userId=userId, user=user)


@app.route('/delete', methods=['POST'])
@login_required
def delete():

    pathId = request.form.get('pathId')
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        if(pathId != None):
            cur = conn.cursor()
            cur.execute("DELETE FROM lpaths WHERE id=%s ;", (int(pathId),))
            return Response("DELETE DONE", status=201, mimetype='application/json')
        return Response("DELETE FAILED", status=400, mimetype='application/json')


@app.route('/deleteAccount', methods=['POST'])
@login_required
def deleteAccount():

    userId = request.get_json()
    with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
        if(userId != None):
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE id=%s ;", (int(userId),))
            cur.execute("DELETE FROM lpaths WHERE userId=%s ;", (int(userId),))
            return Response("DELETE DONE", status=201, mimetype='application/json')
        return Response("DELETE FAILED", status=400, mimetype='application/json')


@app.route('/controlpanel', methods=['GET', 'POST'])
def controlPanel():
    active = [0, 0, 0]
    if request.method == 'POST':
        password = request.form.get('password')
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT password FROM admin WHERE id = 1")
            password = cur.fetchall()[0][0]
            if not password:
                return redirect('/')
            if password != password:
                return redirect('/')
            cur.execute(
                "SELECT * FROM lpaths WHERE isActive = 0")
            evals = cur.fetchall()
            cur.execute(
                "SELECT * FROM lpaths WHERE isActive = 1")
            submissions = cur.fetchall()
            if not evals:
                evals = None

            if not submissions:
                submissions = None

        return render_template("controlpanel.html", active=active, admin=1, evals=evals, submissions=submissions)
    else:

        return render_template("controlpanel.html", active=active)


@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changePassword():
    active = [0, 0, 0]
    if request.method == 'POST':
        userId = session['user_id']
        old = request.form.get('old')
        password = request.form.get('password')
        try:
            with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
                cur = conn.cursor()
                passwordHash = cur.execute(
                    "SELECT passwordhash FROM users WHERE id = %s", (int(userId),)).fetchall()[0][0]
                if passwordHash != None:
                    hash = generate_password_hash(
                        old, method='pbkdf2:sha256', salt_length=8)
                    if check_password_hash(passwordHash, old):
                        newHash = hash = generate_password_hash(
                            password, method='pbkdf2:sha256', salt_length=8)
                        cur.execute(
                            "UPDATE users SET passwordhash = %s WHERE id = %s;", (newHash, userId))
                        return render_template("changepassword.html", active=active, passwordChange="Password changed")
                    return render_template("changepassword.html", active=active, passwordError="Incorrect password")
                else:
                    return render_template("changepassword.html", active=active, passwordChange="Password not changed")
        except Exception as error:
            return print(f"error: {error}")
    else:
        return render_template("changepassword.html", active=active)


@app.route('/verdict', methods=['POST'])
@login_required
def verdict():
    id = request.form.get('pathId')
    verdict = request.form.get('verdict')
    try:
        with psycopg2.connect(DATABASE_URL, sslmode='require') as conn:
            cur = conn.cursor()
            if (verdict):
                cur.execute(
                    "UPDATE lpaths SET isActive = 1 WHERE id = %s;", (id,))
            else:
                cur.execute("DELETE FROM lpaths WHERE id = %s;", (id,))
    except Exception as error:
        return print(f"error: {error}")
    return Response("Verdict made", status=200, mimetype='application/json')
