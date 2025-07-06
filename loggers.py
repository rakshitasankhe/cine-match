import psycopg2
from datetime import datetime

DB_PARAMS = {
    "dbname": "cine_match_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def log_user_mood(username, mood):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        # Get user_id from username
        cur.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user_id = cur.fetchone()
        if not user_id:
            return
        # Insert mood log with current timestamp
        cur.execute(
            "INSERT INTO UserMoodLogs (user_id, mood, log_date) VALUES (%s, %s, %s)",
            (user_id[0], mood, datetime.now())
        )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error logging user mood:", e)

def log_user_interaction(username, movie_id, clicked=True, watch_duration=None):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        # Get user_id from username
        cur.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        user_id = cur.fetchone()
        if not user_id:
            return
        # Insert user interaction (clicked/watch time) with timestamp
        cur.execute("""
            INSERT INTO UserInteractions (user_id, movie_id, clicked, watch_duration, interaction_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id[0], movie_id, clicked, watch_duration, datetime.now()))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print("Error logging user interaction:", e)
