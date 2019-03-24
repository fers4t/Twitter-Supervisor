from twittersupervisor import Database, ConfigFileParser

db = Database(ConfigFileParser('config.json').get_database_credentials())
connection, cursor = db.open_connection()
cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id BIGINT)")
cursor.execute("CREATE TABLE IF NOT EXISTS followers (followed_id BIGINT NOT NULL ,follower_id BIGINT NOT NULL)")
cursor.execute("CREATE TABLE IF NOT EXISTS friendship_events"
               "(followed_id BIGINT, follower_id BIGINT, event_date TIMESTAMP, follows BOOLEAN)")
connection.commit()
connection.close()

