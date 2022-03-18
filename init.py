"""
TODO: update file

RUN THIS FILE ONCE, WILL UPDATE OR CREATE THE DATABASES

The reason for the many try / pass blocks is that there is no way to create a column if it doesn't exist built BIGINTo SQLite
"""
import psycopg2
from struc import db

def update_db():
    db.create("settings", "guild_id BIGINT PRIMARY KEY NOT NULL, prefix VARCHAR")
    db.create("suggestions", "guild_id BIGINT PRIMARY KEY NOT NULL, channel_id BIGINT, type VARCHAR")
    db.create("chatbot", "guild_id BIGINT PRIMARY KEY NOT NULL, channel_id BIGINT")
    db.create("warnings", "guild_id BIGINT, user_id BIGINT, mod_id BIGINT, reason VARCHAR, id BIGINT")
    db.create("tickets", "guild_id BIGINT, ticket_category_id BIGINT, ticket_mod_roles VARCHAR, ticket_log_channel_id BIGINT, ticket_open_message VARCHAR")
    db.create("ticket_data", "guild_id BIGINT, channel_id BIGINT, name VARCHAR, creator_id BIGINT, closed_by_id BIGINT, open_time VARCHAR, close_time VARCHAR, ticket_open_reason VARCHAR, transcript VARCHAR")
    db.create("reaction_roles", "guild_id BIGINT, message_id BIGINT, role_id BIGINT, emoji VARCHAR")

    # Guild DB
        # Settings Table
    
    db.modify("ALTER TABLE settings ADD COLUMN IF NOT EXISTS guild_id BIGINT PRIMARY KEY NOT NULL")



    db.modify("ALTER TABLE settings ADD COLUMN IF NOT EXISTS prefix VARCHAR")


    # Suggestions Table

    db.modify("ALTER TABLE suggestions ADD COLUMN IF NOT EXISTS guild_id BIGINT PRIMARY KEY NOT NULL")



    db.modify("ALTER TABLE suggestions ADD COLUMN IF NOT EXISTS channel_id BIGINT")



    db.modify("ALTER TABLE suggestions ADD COLUMN IF NOT EXISTS type VARCHAR")


    # Chatbot Table

    db.modify("ALTER TABLE chatbot ADD COLUMN IF NOT EXISTS guild_id BIGINT PRIMARY KEY NOT NULL")



    db.modify("ALTER TABLE chatbot ADD COLUMN IF NOT EXISTS channel_id BIGINT")


    # Warnings Table

    db.modify("ALTER TABLE warnings ADD COLUMN IF NOT EXISTS guild_id BIGINT")



    db.modify("ALTER TABLE warnings ADD COLUMN IF NOT EXISTS user_id BIGINT")



    db.modify("ALTER TABLE warnings ADD COLUMN IF NOT EXISTS mod_id BIGINT")



    db.modify("ALTER TABLE warnings ADD COLUMN IF NOT EXISTS reason VARCHAR")



    db.modify("ALTER TABLE warnings ADD COLUMN IF NOT EXISTS id BIGINT")


# Tickets Table

    db.modify("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS guild_id BIGINT")



    db.modify("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS ticket_category_id BIGINT")



    db.modify("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS ticket_mod_roles VARCHAR")



    db.modify("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS ticket_log_channel_id BIGINT")



    db.modify("ALTER TABLE tickets ADD COLUMN IF NOT EXISTS ticket_open_message VARCHAR")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS guild_id BIGINT")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS channel_id BIGINT")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS name VARCHAR")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS creator_id BIGINT")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS closed_by_id BIGINT")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS open_time VARCHAR")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS close_time VARCHAR")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS ticket_open_reason VARCHAR")



    db.modify("ALTER TABLE ticket_data ADD COLUMN IF NOT EXISTS transcript VARCHAR")


# reaction_roles table 

    db.modify("ALTER TABLE reaction_roles ADD COLUMN IF NOT EXISTS guild_id BIGINT")



    db.modify("ALTER TABLE reaction_roles ADD COLUMN IF NOT EXISTS message_id BIGINT")


    db.modify("ALTER TABLE reaction_roles ADD COLUMN IF NOT EXISTS role_id BIGINT")

    db.modify("ALTER TABLE reaction_roles ADD COLUMN IF NOT EXISTS emoji VARCHAR")