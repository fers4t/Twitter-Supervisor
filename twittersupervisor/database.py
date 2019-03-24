from datetime import datetime
import logging
import psycopg2


class Database:

    def __init__(self, database_credentials):
        try:
            self.database_name = database_credentials["database"]
            self.host = database_credentials["host"]
            self.user = database_credentials["user"]
            self.password = database_credentials["password"]
        except KeyError as key_error:
            logging.critical("Invalid \"database_credentials\" argument: {}".format(key_error.args[0]))
            raise
        except TypeError as type_error:
            logging.critical("Incorrect \"database_credentials\" argument: {}".format(type_error.args[0]))
            raise

    def open_connection(self):
        connection = psycopg2.connect(host=self.host, database=self.database_name, user=self.user,
                                      password=self.password)
        return connection, connection.cursor()

    def get_users(self):
        connection, cursor = self.open_connection()
        cursor.execute("SELECT * FROM users")
        users_list = cursor.fetchone()
        connection.close()
        return users_list

    def get_previous_followers_set(self, user_id):
        connection, cursor = self.open_connection()
        cursor.execute("SELECT * FROM followers WHERE followed_id=%s", [user_id])
        previous_followers_list = cursor.fetchall()
        connection.close()
        previous_followers = set()
        for follower in previous_followers_list:
            previous_followers.add(int(follower[0]))
        return previous_followers

    def update_followers_table(self, user_id, new_followers, traitors):
        connection, cursor = self.open_connection()

        # Update "followers" table
        cursor.executemany("DELETE FROM followers WHERE followed_id=%s AND follower_id=%s",
                           self.id_generator(user_id, traitors))
        cursor.executemany("INSERT INTO followers(followed_id, follower_id) VALUES(%s, %s)",
                           self.id_generator(user_id, new_followers))

        # Update "friendship_events" table
        cursor.executemany("INSERT INTO friendship_events(followed_id, follower_id, event_date, follows)"
                           "VALUES(%s,%s,%s,%s)", self.event_generator(user_id, new_followers, True))
        cursor.executemany("INSERT INTO friendship_events(followed_id, follower_id, event_date, follows)"
                           "VALUES(%s,%s,%s,%s)", self.event_generator(user_id, traitors, False))

        connection.commit()
        connection.close()

    @staticmethod
    def id_generator(user_id, followers_set):
        for follower_id in followers_set:
            yield (user_id, follower_id,)

    @staticmethod
    def event_generator(followed_id, followers_set, is_a_follower):
        for follower_id in followers_set:
            yield (followed_id, follower_id, datetime.now(), is_a_follower,)
