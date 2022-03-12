"""
RUN THIS FILE ONCE, WILL UPDATE OR CREATE THE DATABASES

The reason for the many try / pass blocks is that there is no way to create a column if it doesn't exist built into SQLite
"""

import sqlite3
from struc import database
db = database

# Create database tables with their columns if the don't exist
db.create("bot", "config", "token TEXT, owners TEXT")
db.create("guild", "settings", "guild_id INT PRIMARY KEY NOT NULL, prefix TEXT")
db.create("guild", "suggestions", "guild_id INTEGER PRIMARY KEY NOT NULL, channel_id INTEGER, type TEXT")
db.create("guild", "chatbot", "guild_id INTEGER PRIMARY KEY NOT NULL, channel_id INTEGER")
db.create("guild", "warnings", "guild_id INTEGER, user_id INTEGER, mod_id INTEGER, reason TEXT, id INTEGER")
db.create("guild", "tickets", "guild_id INTEGER, ticket_category_id INTEGER, ticket_mod_roles TEXT, ticket_log_channel_id INTEGER, ticket_open_message TEXT")
db.create("guild", "ticket_data", "guild_id INTEGER, channel_id INTEGER, name TEXT, creator_id INTEGER, closed_by_id INTEGER, open_time TEXT, close_time TEXT, ticket_open_reason TEXT, transcript TEXT")

# Bot DB
    # Config Table
try:
    db.modify("bot", "ALTER TABLE config ADD COLUMN token TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("bot", "ALTER TABLE config ADD COLUMN owners TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

# Guild DB
    # Settings Table
try:
    db.modify("guild", "ALTER TABLE settings ADD COLUMN guild_id INT PRIMARY KEY NOT NULL")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE settings ADD COLUMN prefix TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

    # Suggestions Table
try:
    db.modify("guild", "ALTER TABLE suggestions ADD COLUMN guild_id INTEGER PRIMARY KEY NOT NULL")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE suggestions ADD COLUMN channel_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE suggestions ADD COLUMN type TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

    # Chatbot Table
try:
    db.modify("guild", "ALTER TABLE chatbot ADD COLUMN guild_id INTEGER PRIMARY KEY NOT NULL")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE chatbot ADD COLUMN channel_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

    # Warnings Table
try:
    db.modify("guild", "ALTER TABLE warnings ADD COLUMN guild_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE warnings ADD COLUMN user_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE warnings ADD COLUMN mod_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE warnings ADD COLUMN reason TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE warnings ADD COLUMN id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

# Tickets Table
try:
    db.modify("guild", "ALTER TABLE tickets ADD COLUMN guild_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE tickets ADD COLUMN ticket_category_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE tickets ADD COLUMN ticket_mod_roles TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE tickets ADD COLUMN ticket_log_channel_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE tickets ADD COLUMN ticket_open_message TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN guild_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN channel_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN name TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN creator_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN closed_by_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN open_time TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN close_time TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN ticket_open_reason TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE ticket_data ADD COLUMN transcript TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

# reaction_roles table is
try:
    db.modify("guild", "ALTER TABLE reaction_roles ADD COLUMN message_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE reaction_roles ADD COLUMN role_id INTEGER")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass

try:
    db.modify("guild", "ALTER TABLE reaction_roles ADD COLUMN emoji TEXT")
except sqlite3.OperationalError: # Just ignore the error if the column already exists
    pass