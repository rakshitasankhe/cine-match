import psycopg2
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Optional, Tuple

# ------------------------- DB CONFIG -------------------------
DB_NAME = "cine_match_db"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# ----------------------- DATA FETCH --------------------------
def fetch_movies_and_ratings() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Return movies df and ratings df."""
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM Movies")
        movies = pd.DataFrame(cur.fetchall(), columns=[c.name for c in cur.description])

        cur.execute("SELECT * FROM Ratings")
        ratings = pd.DataFrame(cur.fetchall(), columns=[c.name for c in cur.description])

    return movies, ratings

# ------------------- RECOMMENDER CORE ------------------------
def recommend_movies(
    user_id: int,
    current_mood: str,
    top_n: int = 10,
    genre: Optional[str] = None,
    language: Optional[str] = None,
    duration_range: Optional[Tuple[int, int]] = None,   # (min, max) in minutes
    year_range: Optional[Tuple[int, int]] = None        # (start, end)
) -> pd.DataFrame:
    """
    Hybrid recommendation:
      • TF‑IDF on mood_tags (content)
      • Mean community rating (collaborative proxy)
    Plus optional filters.
    """

    # ----- load data -----
    movies, ratings = fetch_movies_and_ratings()

    # ----- optional filters -----
    if genre:
        movies = movies[movies['genre'].str.contains(genre, case=False, na=False)]
    if language:
        movies = movies[movies['language'].str.contains(language, case=False, na=False)]
    if duration_range:
        movies = movies[
            (movies['duration'] >= duration_range[0]) &
            (movies['duration'] <= duration_range[1])
        ]
    if year_range:
        movies = movies[
            (movies['release_year'] >= year_range[0]) &
            (movies['release_year'] <= year_range[1])
        ]

    if movies.empty:
        return pd.DataFrame(columns=['title', 'reason'])

    # ----- content (mood similarity) -----
    tfidf = TfidfVectorizer()
    tfidf_matrix = tfidf.fit_transform(movies['mood_tags'].fillna(''))
    mood_vec      = tfidf.transform([current_mood])
    movies['sim_mood'] = cosine_similarity(mood_vec, tfidf_matrix).flatten()

    # ----- collaborative (mean rating) -----
    mean_ratings = ratings.groupby('movie_id')['rating'].mean()
    movies = movies.merge(mean_ratings, how='left',
                          left_on='movie_id', right_index=True)
    movies.rename(columns={'rating': 'avg_rating'}, inplace=True)
    movies['avg_rating'].fillna(movies['avg_rating'].mean(), inplace=True)

    # ----- blend scores -----
    w_content = 0.6
    w_collab  = 0.4
    movies['score'] = (
        w_content * movies['sim_mood'] +
        w_collab  * (movies['avg_rating'] / 5)  # normalise to 0‑1
    )

    movies = movies.sort_values('score', ascending=False).head(top_n)

    return movies[['title', 'genre', 'language',
                   'duration', 'mood_tags',
                   'avg_rating', 'score']]
