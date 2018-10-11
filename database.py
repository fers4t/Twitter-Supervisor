import sqlite3

def openConnection():
  connection = sqlite3.connect('followers.db')
  return connection, connection.cursor()

def get_previous_followers_set():
    connection, cursor = openConnection()
    cursor.execute('CREATE TABLE IF NOT EXISTS followers (id integer)')
    connection.commit()
    cursor.execute('SELECT * FROM followers')
    previous_followers_list = cursor.fetchall()
    connection.close()
    previous_followers = set()
    for follower in previous_followers_list:
        previous_followers.add(int(follower[0]))
    return previous_followers

def id_generator(followersSet):
    for id in followersSet:
        yield (id,)

def save_followers_set(followersSet):
    # TODO: Solve the bug preventing sometimes to save the last follower
    connection, cursor = openConnection()
    cursor.execute('DELETE FROM followers')
    cursor.executemany("INSERT INTO followers(id) VALUES(?)", id_generator(followersSet))
    connection.commit()
    connection.close()
