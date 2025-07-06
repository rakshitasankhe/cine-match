import psycopg2

DB_PARAMS = {
    "dbname": "cine_match_db",
    "user": "your_username",
    "password": "your_password",
    "host": "localhost",
    "port": "5432"
}

def predict_mood(description):
    description = description.lower() if description else ""
    moods = []
    # Simple keyword-based mood detection
    if any(word in description for word in ['love', 'romance', 'heart']):
        moods.append('romantic')
    if any(word in description for word in ['happy', 'joy', 'fun']):
        moods.append('happy')
    if any(word in description for word in ['scary', 'ghost', 'horror']):
        moods.append('scary')
    if any(word in description for word in ['thrill', 'action', 'chase']):
        moods.append('thrilling')
    if any(word in description for word in ['sad', 'cry', 'loss']):
        moods.append('sad')
    return ','.join(moods) if moods else 'neutral'

def update_mood_tags():
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT movie_id, description FROM Movies")
    movies = cur.fetchall()
    for movie_id, description in movies:
        mood_tags = predict_mood(description)
        # Update mood_tags column for each movie
        cur.execute("UPDATE Movies SET mood_tags = %s WHERE movie_id = %s", (mood_tags, movie_id))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    update_mood_tags()
    print("Movies mood_tags updated.")
