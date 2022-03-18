import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

hostname = os.environ.get("HOSTNAME")
database = os.environ.get("DATABASE")
user = os.environ.get("DB_USER")
password = os.environ.get("PASSWORD")
port = os.environ.get("PORT")

if os.getenv("HOSTNAME"):
    hostname = os.getenv("HOSTNAME")

if os.getenv("DATABASE"):
    database = os.getenv("DATABASE")

if os.getenv("USERNAME"):
    user = os.getenv("DB_USER")

if os.getenv("PASSWORD"):
    password = os.getenv("PASSWORD")

if os.getenv("PORT"):
    port = os.getenv("PORT")

conn = psycopg2.connect(
    host = hostname,
    dbname = database,
    user = user,
    password = password,
    port = port
)

def fetch(sql, binds=None):
    cur = conn.cursor()

    if binds is None:
        cur.execute(sql)
    else:
        cur.execute(sql, binds)
    fetch = cur.fetchone()

    cur.close()
    #conn.close()
    
    if fetch is not None:
        return fetch[0]
    else:
        return fetch

def fetchall(sql, binds=None):
    cur = conn.cursor()

    if binds is None:
        cur.execute(sql)
    else:
        cur.execute(sql, binds)

    fetch = cur.fetchall()

    cur.close()
    #conn.close()

    return fetch


def modify(sql, binds=None):
    cur = conn.cursor()

    if binds is None:
        cur.execute(sql)
    else:
        cur.execute(sql, binds)
    conn.commit()

    cur.close()
    #conn.close()

def create(table, columns):
    cur = conn.cursor()

    cur.execute(f"CREATE TABLE IF NOT EXISTS {table}({columns});")
    conn.commit()

    cur.close()
    #conn.close()