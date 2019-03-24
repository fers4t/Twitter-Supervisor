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

    def get_previous_followers_set(self):
        connection, cursor = self.open_connection()
        cursor.execute("CREATE TABLE IF NOT EXISTS followers (id BIGINT NOT NULL)")
        connection.commit()
        cursor.execute("SELECT * FROM followers")
        previous_followers_list = cursor.fetchall()
        connection.close()
        previous_followers = set()
        for follower in previous_followers_list:
            previous_followers.add(int(follower[0]))
        return previous_followers

    def update_followers_table(self, new_followers, traitors):
        connection, cursor = self.open_connection()

        # Populate "followers" table
        cursor.executemany("DELETE FROM followers WHERE id=%s", self.id_generator(traitors))
        cursor.executemany("INSERT INTO followers(id) VALUES(%s)", self.id_generator(new_followers))

        # Create & populate "friendship_events" table
        cursor.execute("CREATE TABLE IF NOT EXISTS friendship_events"
                       "(user_id BIGINT, event_date TIMESTAMP, follows BOOLEAN)")
        cursor.executemany("INSERT INTO friendship_events(user_id, event_date, follows) VALUES(%s,%s,%s)",
                           self.event_generator(new_followers, True))
        cursor.executemany("INSERT INTO friendship_events(user_id, event_date, follows) VALUES(%s,%s,%s)",
                           self.event_generator(traitors, False))

        connection.commit()
        connection.close()

    @staticmethod
    def id_generator(followers_set):
        for user_id in followers_set:
            yield (user_id,)

    @staticmethod
    def event_generator(users_set, is_a_follower):
        for user_id in users_set:
            yield (user_id, datetime.now(), is_a_follower,)
