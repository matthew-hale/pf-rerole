import os
import sqlite3

DATA_DIR = os.environ.get("PF_REROLE_DATA_DIR", "./")
DB_NAME = "pf-rerole.db"
DB_PATH = DATA_DIR + DB_NAME

user_table = """CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    username TEXT
)"""

character_table = """CREATE TABLE IF NOT EXISTS character(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    name TEXT,
    data TEXT,
    FOREIGN KEY(user_id) REFERENCES user(id)
)"""

def get_con():
    con = sqlite3.connect(DB_PATH)
    con.autocommit = False
    return con

def init():
    with get_con() as con:
        cur = con.cursor()
        cur.execute(user_table)
        cur.execute(character_table)
        con.commit()

def get_uid(username: str) -> int:
    """If a user is not currently in the database, this function will also insert it."""
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT id FROM user WHERE username=?", (username,))
        data = res.fetchone()
        if data:
            return data[0]

        cur.execute("INSERT INTO user (username) VALUES (?)", (username,))
        con.commit()
        res = cur.execute("SELECT id FROM user WHERE username=?", (username,))
        data = res.fetchone()
        return data[0]
