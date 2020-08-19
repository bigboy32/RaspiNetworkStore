import hashlib
import sqlite3
import os
from flask import *


app = Flask(__name__)
app.secret_key = "some random string!!!"

app.config['UPLOAD_DIR'] = "UploadedFiles/"


def _hash(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


try:
    open("Userdb.db", "r")
    created = True
except:
    created = False

conn = sqlite3.connect("Userdb1.db", check_same_thread=False)
cur = conn.cursor()

cur.execute(
    "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"
)


def exists(username):
    cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))
    if cur.fetchall() != []:
        return True
    else:
        return False


if not exists("admin"):
    cur.execute(
        "INSERT INTO users VALUES ('admin', '{}')".format(_hash('admin')))

conn.commit()


@app.route("/")
def firstPage():
    session["logedIn"] = False
    session["username"] = None

    return redirect("/login")


@app.route("/index")
def index():
    if not session["logedIn"]:
        return redirect("/login")
    else:
        return render_template("index.html", name=session["username"])


@app.route("/login")
def _login():
    if session["logedIn"]:
        return redirect("/index")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def __login():
    if exists(request.form["uname"]):
        cur.execute("SELECT password FROM users WHERE username='{}'".format(
            request.form["uname"]))
        data = cur.fetchall()
        print(data)
        if data != []:
            if data[0][0] == _hash(request.form["passwd"]):
                session["username"] = request.form["uname"]
                session["logedIn"] = True
                return redirect("/index")
            else:
                return redirect("/login")
    else:
        return redirect("/login")


@app.route("/register")
def register():
    if session["logedIn"]:
        return render_template("register.html")
    return redirect("/")


@app.route("/register", methods=["POST"])
def register_():
    if not exists(request.form["uname"]):
        if request.form["passwd"] == request.form["passwd_conf"]:
            cur.execute(
                "INSERT INTO users VALUES ('{}', '{}')".format(request.form["uname"], _hash(request.form["passwd"])))
            conn.commit()
            return redirect("/index")
        else:
            return redirect("/register")
    else:
        return redirect("/register")


@app.route("/logout")
def logout():
    session["logedIn"] = False
    return redirect("/")


@app.route("/download")
def download():
    if session["logedIn"]:
        uf = os.listdir("UploadedFiles")
        return render_template("downloads.html", items=uf)


@app.route("/download", methods=["POST"])
def download_():
    uf = os.listdir("UploadedFiles")
    return send_file(os.path.join("UploadedFiles", uf[int(request.form["number"]) - 1]), attachment_filename=uf[int(request.form["number"]) - 1])


@app.route("/upload")
def upload():
    if session["logedIn"]:
        return render_template("uploads.html")


@app.route("/upload", methods=["POST"])
def upload_():
    f = request.files['file']
    print(f.filename)
    f.save("UploadedFiles/" + f.filename)
    return 'file uploaded successfully'


app.run(debug=True, host='0.0.0.0', port=3000)
