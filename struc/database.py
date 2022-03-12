"""
Managing the bot's databases here.
WHEN THE BOT REACH MORE MEMBERS AND SERVERS, THE GUILD DB SHOULD BE CONSTANTLY OPEN !!!
"""
import sqlite3


def fetch(db, sql, bind=None):
    """
    Fetches the database and returns one value only
    ### Parameters:
    1. db ('guild' or 'bot') :: REQUIRED
    2. sql (sql commands) :: REQUIRED
    3. bind (use bindings) :: OPTIONAL
    
    """
    guild_db = sqlite3.connect("guild_data.db")
    guild_cur = guild_db.cursor()
    bot_db = sqlite3.connect("bot_data.db")
    bot_cur = bot_db.cursor()

    if db == "bot":
        #set_db = bot_db
        set_cur = bot_cur
    else:
        #set_db = guild_db
        set_cur = guild_cur
    try:
        if not bind:
            output = set_cur.execute(sql)
        else:
            output = set_cur.execute(sql,bind)
        fetch = output.fetchone()
        if not fetch:
            return fetch
        else:
            return fetch[0]
    except Exception as err:
        print(err)

    guild_db.close()
    bot_db.close()

def fetchall(db, sql, bind=None):
    """
    Fetches the database and returns all values
    ### Parameters:
    1. db ('guild' or 'bot') :: REQUIRED
    2. sql (sql commands) :: REQUIRED
    3. bind (use bindings) :: OPTIONAL
    
    """
    guild_db = sqlite3.connect("guild_data.db")
    guild_cur = guild_db.cursor()
    bot_db = sqlite3.connect("bot_data.db")
    bot_cur = bot_db.cursor()

    if db == "bot":
        #set_db = bot_db
        set_cur = bot_cur
    else:
        #set_db = guild_db
        set_cur = guild_cur
    try:
        if not bind:
            output = set_cur.execute(sql)
        else:
            output = set_cur.execute(sql,bind)
        fetch = output.fetchall()
        if not fetch:
            return fetch
            
        else:
            return fetch
    except Exception as err:
        print(err)

    guild_db.close()
    bot_db.close()

def modify(db, sql, bind=None):
    """
    Modifies the database and commit the changes
    ### Parameters:
    1. db ('guild' or 'bot') :: REQUIRED
    2. sql (sql commands) :: REQUIRED
    3. bind (use bindings) :: OPTIONAL
    
    """
    guild_db = sqlite3.connect("guild_data.db")
    guild_cur = guild_db.cursor()
    bot_db = sqlite3.connect("bot_data.db")
    bot_cur = bot_db.cursor()

    if db == "bot":
        set_db = bot_db
        set_cur = bot_cur
    else:
        set_db = guild_db
        set_cur = guild_cur
    if not bind:
        set_cur.execute(sql)
    else:
        set_cur.execute(sql,bind)

    set_db.commit()

    guild_db.close()
    bot_db.close()


def create(db, table, columns):
    """
    Adds a table to the given database
    ### Parameters:
    1. db ('guild' or 'bot') :: REQUIRED
    2. table (the name of the table) :: REQUIRED
    3. columns (the name of the columns) :: OPTIONAL
    
    """
    guild_db = sqlite3.connect("guild_data.db")
    guild_cur = guild_db.cursor()
    bot_db = sqlite3.connect("bot_data.db")
    bot_cur = bot_db.cursor()

    if db == "bot":
        set_db = bot_db
        set_cur = bot_cur
    else:
        set_db = guild_db
        set_cur = guild_cur
    try:
        set_cur.execute(f"CREATE TABLE IF NOT EXISTS {table}({columns})")
        set_db.commit()
    except Exception as err:
        print(err)

    guild_db.close()
    bot_db.close()