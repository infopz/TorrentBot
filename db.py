import sqlite3


def get_last():
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM magnet ORDER BY magnetid DESC LIMIT 1;")
        d = cur.fetchone()
    return {"number": d[0], "name": d[1], "magnet": d[2]}


def write_magnet(title, magnet):
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO magnet(title, magnetlink) VALUES (?,?);", (title, magnet))
        rid = cur.lastrowid
        cur.execute("UPDATE magnet SET magnetid=? WHERE ROWID=?;", (rid, rid))
    return rid


def check_magnet(num):
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT magnetlink FROM magnet WHERE magnetid=?", (num,))
        n = cur.fetchone()[0]
    return n


def get_magnet(num):
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM magnet WHERE magnetid=?", (num,))
        n = cur.fetchone()
    return n


def add_torrent(title, completed):
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO torrents VALUES (?, ?)", (title, completed))


def get_torrent(title):
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM torrents WHERE name=?", (title,))
        t = cur.fetchone()
    return t


def torrent_completed(title):
    conn = sqlite3.connect("db.sql")
    with conn:
        cur = conn.cursor()
        cur.execute("UPDATE torrents SET completed=1 WHERE name=?", (title,))
