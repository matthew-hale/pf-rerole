import bcrypt
import json
import os
import sqlite3

DATA_DIR = os.environ.get("PF_REROLE_DATA_DIR", "./")
DB_NAME = "pf-rerole.db"
DB_PATH = DATA_DIR + DB_NAME

TABLE_DEFINITIONS = {
    "auth_method": """
        CREATE TABLE IF NOT EXISTS auth_method(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL)
    """,
    "user": """
        CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        disabled INTEGER NOT NULL DEFAULT 0,
        auth_method_id INTEGER NOT NULL,
        email TEXT NOT NULL,
        password TEXT,

        UNIQUE(auth_method_id, email),

        FOREIGN KEY(auth_method_id) REFERENCES auth_method(id)
        )
    """,
    "role": """
        CREATE TABLE IF NOT EXISTS role(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
        )
    """,
    "user_role": """
        CREATE TABLE IF NOT EXISTS user_role(
        user_id INTEGER NOT NULL,
        role_id INTEGER NOT NULL,

        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
        FOREIGN KEY(role_id) REFERENCES role(id)

        PRIMARY KEY(user_id, role_id)
        )
    """,
    "permission": """
        CREATE TABLE IF NOT EXISTS permission(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """,
    "role_permission": """
        CREATE TABLE IF NOT EXISTS role_permission(
        role_id INTEGER NOT NULL,
        permission_id INTEGER NOT NULL,

        FOREIGN KEY(role_id) REFERENCES role(id) ON DELETE CASCADE,
        FOREIGN KEY(permission_id) REFERENCES permission(id) ON DELETE CASCADE,

        PRIMARY KEY(role_id, permission_id)
        )
    """,
    "token_type": """
        CREATE TABLE IF NOT EXISTS token_type(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """,
    "auth_token": """
        CREATE TABLE IF NOT EXISTS auth_token(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        token_type_id INTEGER NOT NULL,
        token TEXT UNIQUE NOT NULL,
        created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
        last_used TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE,
        FOREIGN KEY(token_type_id) REFERENCES token_type(id)
        )
    """,
    "character": """
        CREATE TABLE IF NOT EXISTS character(
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT,
        data TEXT,
        FOREIGN KEY(user_id) REFERENCES user(id) ON DELETE CASCADE
        )
    """,
}

DEFAULT_PERMISSIONS = [
    "create_character",
    "read_owned_character",
    "update_owned_character",
    "delete_owned_character",
    "read_any_character",
    "delete_any_character",
]
_permission_insert_values = ", ".join(['("' + x + '")' for x in DEFAULT_PERMISSIONS])

DEFAULT_ROLE_PERMS = {
    "user": [
        "create_character",
        "read_owned_character",
        "update_owned_character",
        "delete_owned_character",
    ],
    "admin": [
        "read_any_character", "delete_any_character"
    ],
}

_role_insert_values = ", ".join(['("' + x + '")' for x in DEFAULT_ROLE_PERMS.keys()])
TABLE_INSERTS = {
    "auth_method": 'INSERT OR IGNORE INTO auth_method (name) VALUES ("github"), ("rerole")',
    "role": 'INSERT OR IGNORE INTO role (name) VALUES' + _role_insert_values,
    "permission": 'INSERT OR IGNORE INTO permission (name) VALUES' + _permission_insert_values,
    "token_type": 'INSERT OR IGNORE INTO token_type (name) VALUES ("session"), ("API")',
}

def get_con():
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON");
    con.autocommit = False
    return con

def init():
    with get_con() as con:
        cur = con.cursor()
        for _, t in TABLE_DEFINITIONS.items():
            cur.execute(t)
        for _, i in TABLE_INSERTS.items():
            cur.execute(i)
        role_perm_insert_statement = """
            INSERT OR IGNORE INTO role_permission (role_id, permission_id)
                      SELECT role.id, permission.id
                        FROM role, permission
                       WHERE role.name=?
                         AND permission.name=?
        """
        for role in DEFAULT_ROLE_PERMS:
            for permission in DEFAULT_ROLE_PERMS[role]:
                cur.execute(role_perm_insert_statement, (role, permission,))
        con.commit()


def create_user(method: str,
                email: str,
                roles: list = ["user"],
                password=None) -> int:
    """Creates a user in the database, returning the new user id."""
    if method == "rerole.app" and password is None:
        return None

    if password is not None:
        password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    user_insert_statement = """
    INSERT INTO user (auth_method_id, email, password)
         SELECT id, ?, ?
           FROM auth_method
          WHERE auth_method.name = ?
      RETURNING user.id"""
    user_insert_values = (email, password, method,)

    user_role_insert_statement = """
    INSERT INTO user_role (user_id, role_id)
         SELECT ?, role.id
           FROM role
          WHERE role.name = ?"""
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(user_insert_statement, user_insert_values)
        data = res.fetchone()
        user_id = data[0]

        for role in roles:
            user_role_insert_values = (user_id, role,)
            cur.execute(user_role_insert_statement, user_role_insert_values)

        con.commit()
    return user_id

def get_user_id(method: str, email: str) -> int:
    user_id_stmt = """
    SELECT id
      FROM user
     WHERE auth_method_id=(
           SELECT id
             FROM auth_method
            WHERE name=?
           )
       AND email=?
    """
    values = (method, email,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(user_id_stmt, values)
        data = res.fetchone()
    if data is None:
        return None
    return data[0]

def user_exists(method: str, email: str) -> bool:
    user_exists_statement = """
    SELECT true
      FROM user
     WHERE auth_method_id=(
           SELECT id
             FROM auth_method
            WHERE name=?
           )
       AND email=?
    """
    values = (method, email,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(user_exists_statement, values)
        data = res.fetchall()

    exists = len(data) == 1
    return exists

def get_user_permissions(user_id: int) -> list:
    select_statement = """
       SELECT p.name
         FROM permission p
              INNER JOIN role_permission rp
                      ON rp.permission_id = p.id
              INNER JOIN role r
                      ON rp.role_id = r.id
        WHERE r.id IN (
              SELECT role_id FROM user WHERE id = ?
              )
    """
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute()
        data = res.fetchall()
    permissions = [x[0] for x in data]
    return permissions

def user_is_disabled(method: str, email: str):
    select_user_statement = """
    SELECT disabled
      FROM user
     WHERE auth_method_id=(
           SELECT id FROM auth_method WHERE name=?
           )
       AND email=?
    """
    select_user_values = (method, email,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(select_user_statement, select_user_values)
        data = res.fetchone()

    if data is None:
        return True
    return bool(data[0])

def authenticate(email: str, password: str) -> bool:
    if user_is_disabled("rerole.app", email):
        return False

    select_hash_statement = """
    SELECT id, password
      FROM user
     WHERE email=?
       AND auth_method_id=(
           SELECT id
             FROM auth_method
            WHERE name="rerole.app"
           )
    """
    select_hash_values = (email,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(select_hash_statement, select_hash_values)
        data = res.fetchone()

    if data is None:
        return False

    user_id = data[0]
    current_hash = data[1]
    new_hash = bcrypt.hashpw(password.encode("utf-8"), current_hash)
    correct_password = new_hash == current_hash
    return correct_password

def create_session_token(user_id: int, token: str):
    insert_token_statement = """
    INSERT INTO auth_token (user_id, token_type_id, token)
         SELECT ?, token_type.id, ?
           FROM token_type
          WHERE token_type.name="session"
    """
    insert_token_values = (user_id, token,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(insert_token_statement, insert_token_values)
        con.commit()

def refresh_auth_token(token: str):
    token_update_statement = """
    UPDATE auth_token
       SET last_used=datetime()
     WHERE token=?
    """
    token_update_values = (token,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(token_update_statement, token_update_values)
        rows = res.fetchall()
        con.commit()


def valid_auth_token(token: str) -> bool:
    valid_token_stmt = """
    SELECT id FROM auth_token WHERE token=?
    """
    values = (token,)
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute(valid_token_stmt, values)
        data = res.fetchall()
    return len(data) == 1


def create_character(user_id: int, data: dict) -> int:
    name = data.get("name", "")
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("INSERT INTO character (user_id, name, data) VALUES (?, ?, ?) RETURNING id", (user_id, name, json.dumps(data),))
        c_id = res.fetchone()
        con.commit()
    return c_id[0]

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


def user_owns_character(user_id, character_id) -> bool:
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT id FROM character WHERE user_id=? AND id=?", (user_id, character_id,))
        data = res.fetchall()
    return len(data) == 1

def get_user_characters(user_id: int) -> list:
    """Return a list of all characters owned by the given user id."""
    with get_con() as con:
        cur = con.cursor()
        res = cur.execute("SELECT id, name FROM character WHERE user_id=?", (user_id,))
        data = res.fetchall()
    if data is None:
        return []

    def tuple_to_dict(d):
        return {
            "id": d[0],
            "name": d[1],
        }
    return list(map(tuple_to_dict, data))
