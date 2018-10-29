import sqlite3


def open_connection():
    connection = sqlite3.connect('followers.db')
    return connection, connection.cursor()


def get_previous_followers_set():
    connection, cursor = open_connection()
    cursor.execute('CREATE TABLE IF NOT EXISTS followers (id integer)')
    connection.commit()
    cursor.execute('SELECT * FROM followers')
    previous_followers_list = cursor.fetchall()
    connection.close()
    previous_followers = set()
    for follower in previous_followers_list:
        previous_followers.add(int(follower[0]))
    return previous_followers


def id_generator(followers_set):
    for id in followers_set:
        yield (id,)


def update(new_followers, unfollowers):
    connection, cursor = open_connection()
    cursor.executemany("DELETE FROM followers WHERE id=?", id_generator(unfollowers))
    cursor.executemany("INSERT INTO followers(id) VALUES(?)", id_generator(new_followers))
    connection.commit()
    connection.close()
