import sqlite3
from datetime import datetime


def open_connection():
    connection = sqlite3.connect("followers.db")
    return connection, connection.cursor()


def get_previous_followers_set():
    connection, cursor = open_connection()
    cursor.execute("CREATE TABLE IF NOT EXISTS followers (id integer)")
    connection.commit()
    cursor.execute("SELECT * FROM followers")
    previous_followers_list = cursor.fetchall()
    connection.close()
    previous_followers = set()
    for follower in previous_followers_list:
        previous_followers.add(int(follower[0]))
    return previous_followers


def id_generator(followers_set):
    for id in followers_set:
        yield (id,)


def event_generator(users_set, true):
    for id in users_set:
        if true:
            yield (id, datetime.today().isoformat(), 1,)
        else:
            yield (id, datetime.today().isoformat(), 1,)


def update_followers_table(new_followers, traitors):
    connection, cursor = open_connection()
    cursor.executemany("DELETE FROM followers WHERE id=?", id_generator(traitors))
    cursor.executemany("INSERT INTO followers(id) VALUES(?)", id_generator(new_followers))
    cursor.execute("CREATE TABLE IF NOT EXISTS friendship_events (user_id integer, event_date text, follows integer)")
    # TODO populate friendships_event
    cursor.executemany("INSERT INTO friendship_events(user_id, event_date, follows) VALUES(?,?,?)", event_generator(new_followers, True))
    connection.commit()
    connection.close()


def insert_betrayals(traitors):
    connection, cursor = open_connection()
    cursor.execute("CREATE TABLE IF NOT EXISTS betrayals (traitor_id integer, betrayal_date text )")
    for traitor_id in traitors:
        new_tuple = [(traitor_id, datetime.today().isoformat())]
        cursor.execute("INSERT INTO betrayals(traitor_id, betrayal_date) VALUES(?, ?)", new_tuple)
    connection.commit()
    connection.close()
