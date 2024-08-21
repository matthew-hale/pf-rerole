import json
import os
import sqlite3

DATA_DIR = os.environ.get("PF_REROLE_DATA_DIR", "./")
DB_NAME = "pf-rerole.db"
DB_PATH = DATA_DIR + DB_NAME

user_table = """CREATE TABLE IF NOT EXISTS user(
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE
)"""

session_table = """CREATE TABLE IF NOT EXISTS session(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    token TEXT,
    last_used TEXT,
    FOREIGN KEY(user_id) REFERENCES user(id)
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
        cur.execute(session_table)
        cur.execute(character_table)
        con.commit()

def get_uid(username: str) -> int:
    """Get the id of the given username.

    If the provided username does not exist in the database, this function will also insert it.
    """
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT id FROM user WHERE username=?", (username,))
        data = res.fetchone()
        if data:
            return data[0]

        res = cur.execute("INSERT INTO user (username) VALUES (?) RETURNING id", (username,))
        data = res.fetchone()
        con.commit()
        return data[0]

def refresh_session(username: str, token):
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT id FROM session WHERE user_id=(SELECT id FROM user WHERE username=?) AND token=?", (username, token,))
        data = res.fetchone()
        if data is None:
            res = cur.execute("INSERT INTO session (user_id, token, last_used) SELECT id, ?, datetime() FROM user WHERE username=?", (token, username,))
            con.commit()
            return
        session_id = data[0]
        res = cur.execute("UPDATE session SET last_used=datetime() WHERE id=?", (session_id,))
        con.commit()

def delete_session(username: str, token):
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("DELETE FROM session WHERE user_id=(SELECT id FROM user WHERE username=?) AND token=?", (username, token,))
        con.commit()

def delete_all_sessions(username: str):
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("DELETE FROM session WHERE user_id=(SELECT id FROM user WHERE username=?)", (username,))

def valid_session(username: str, token) -> bool:
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT true FROM session WHERE user_id=(SELECT id FROM user WHERE username=?) AND token=()", (username, token,))
        data = res.fechone()
    return bool(data)

def create_character(username: str, data: dict) -> int:
    name = data.get("name", "")
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("INSERT INTO character (user_id, name, data) SELECT user.id, ?, ? FROM user WHERE username=? RETURNING id", (name, json.dumps(data), username,))
        cid = res.fetchone()
        con.commit()
    return cid[0]

def get_character(character_id: int) -> dict:
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT data FROM character WHERE id=?", (character_id,))
        data = res.fetchone()
    if data is None:
        return None
    return json.loads(data[0])

def update_character(character_id: int, data: dict):
    name = data.get("name", "")
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("UPDATE character SET name=?, data=? WHERE id=?", (name, json.dumps(data), character_id,))
        con.commit()

def delete_character(character_id: int):
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("DELETE FROM character WHERE id=?", (character_id,))
        con.commit()

def get_user_characters(username: str) -> list:
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT id, name FROM character WHERE user_id=(SELECT id FROM user WHERE username=?)", (username,))
        data = res.fetchall()
    if data is None:
        return []

    def tuple_to_dict(d):
        return {
            "id": d[0],
            "name": d[1],
        }
    return list(map(tuple_to_dict, data))

def user_owns_character(username: str, character_id: int) -> bool:
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT true FROM character WHERE id=? AND user_id=(SELECT id FROM user WHERE username=?)", (character_id, username,))
        data = res.fetchone()
    return bool(data)
