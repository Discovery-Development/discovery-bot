"""
File for getting the server configurations
"""
from . import db

def prefix(client, id_source: int):
    """
    Get the guild prefix
    """
    if id_source.guild == None:
        prefix = None
        return prefix   
    else:
        prefix = db.fetch(f"SELECT prefix FROM settings WHERE guild_id = {id_source.guild.id};")

        if prefix is None:
            db.modify(f"INSERT INTO settings(guild_id, prefix) VALUES ({id_source.guild.id}, '!');")
            prefix = db.fetch(f"SELECT prefix FROM settings WHERE guild_id = {id_source.guild.id};")
        return str(prefix)