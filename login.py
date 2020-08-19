import sqlite3
import hashlib


def _hash(password):
    return hashlib.sha256(password).hexdigest()


def init():

    try:
        open("Userdb.db", "r")
        created = True
    except:
        created = False

    conn = sqlite3.connect("Userdb.db")
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)"
    )

    adduser(cur, "admin", "admin")

    return [conn, cur]


def commit(conn):
    conn.commit()


def exists(cur, username):
    cur.execute("SELECT * FROM users WHERE username = '{}'".format(username))

    if cur.fetchall() != [()]:
        return True
    else:
        return False


def adduser(cur, username, password):

    if not exists(cur, username):
        password = _hash(password)
        cur.execute("INSER INTO users VALUES (username, password)")

        commit()


def ispassword(cur, username, password):
    password = _hash(password)
    cur.execute("SELECT * FROM users WHERE password='{}'".format(password))

    if cur.fetchall() != [()]:
        return True
    else:
        return False
