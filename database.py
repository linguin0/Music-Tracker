import sqlite3

def initialiseDB():
    '''
    Initialised sqlite3 database and creates tables if needed.
    Returns cursor object
    '''
    try:
        connection = sqlite3.connect("TrackerDB.db")
        cursor = connection.cursor()
    except ConnectionRefusedError:
        return "Error: Cannot connect to TrackerDB.db"

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS RELEASE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discog_id INTEGER,
            title VARCHAR(255),
            year INTEGER,
            tracklist VARCHAR(255),
            genre VARCHAR(255),
            format VARCHAR(255),
            image VARCHAR(255)
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS ARTIST (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discog_id INTEGER,
            name VARCHAR(255),
            active BOOLEAN,
            image VARCHAR(255)
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS MEMBER (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            image VARCHAR(255)
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS LABEL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            image VARCHAR(255)
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS USERLIST (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER NOT NULL,
            rating FLOAT,
            wishlist BOOLEAN
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS RELEASE_ARTISTS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER NOT NULL,
            artist_id INTEGER NOT NULL,
            FOREIGN KEY (release_id) REFERENCES RELEASE (id),
            FOREIGN KEY (artist_id) REFERENCES ARTIST(id)
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS ARTIST_MEMBERS (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            FOREIGN KEY (artist_id) REFERENCES ARTIST (id),
            FOREIGN KEY (member_id) REFERENCES MEMBER (id)
        );"""
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS CD_LABEL (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            release_id INTEGER NOT NULL,
            label_id INTEGER NOT NULL,
            FOREIGN KEY (release_id) REFERENCES RELEASE (id)
            FOREIGN KEY (label_id) REFERENCES LABEL (id)
        );"""
    )
    return connection