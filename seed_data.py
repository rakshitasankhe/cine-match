import psycopg2

# Replace with your actual DB credentials
DB_NAME = "cine_match_db"
DB_USER = "postgres"
DB_PASSWORD = "Boka@1231"
DB_HOST = "localhost"
DB_PORT = "5433"

def insert_sample_data():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        # Insert sample users
        cur.execute("""
            INSERT INTO Users (username, email) VALUES
            ('alice', 'alice@example.com'),
            ('bob', 'bob@example.com'),
            ('carol', 'carol@example.com')
            ON CONFLICT DO NOTHING;
        """)

        # Insert sample movies
        cur.execute("""
            INSERT INTO Movies (title, genre, release_year, description, duration, mood_tags, language) VALUES
            ('The Shawshank Redemption', 'Drama', 1994, 'Two imprisoned men bond over years...', 142, 'hopeful,inspiring', 'English'),
            ('Inception', 'Sci-Fi', 2010, 'A thief who steals corporate secrets...', 148, 'thrilling,mind-bending', 'English'),
            ('Amélie', 'Romance', 2001, 'Amélie is an innocent and naive girl...', 122, 'romantic,feel-good', 'French'),
            ('The Conjuring', 'Horror', 2013, 'Paranormal investigators help a family...', 112, 'scary,thrilling', 'English'),
            ('Inside Out', 'Animation', 2015, 'Young girl’s emotions come to life...', 95, 'happy,emotional', 'English')
            ON CONFLICT DO NOTHING;
        """)

        # Insert sample ratings
        cur.execute("""
            INSERT INTO Ratings (user_id, movie_id, rating) VALUES
            (1, 1, 5.0),
            (1, 2, 4.5),
            (2, 3, 4.0),
            (3, 4, 3.5),
            (3, 5, 4.5);
        """)

        # Insert sample mood logs
        cur.execute("""
            INSERT INTO UserMoodLogs (user_id, mood) VALUES
            (1, 'happy'),
            (2, 'thoughtful'),
            (3, 'scared'),
            (1, 'inspired'),
            (2, 'romantic');
        """)

        conn.commit()
        print("✅ Sample data inserted successfully!")

        cur.close()
        conn.close()
    except Exception as e:
        print("❌ Error inserting data:", e)

if __name__ == "__main__":
    insert_sample_data()
