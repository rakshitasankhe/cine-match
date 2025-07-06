from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import psycopg2
import pandas as pd

def fetch_ratings():
    conn = psycopg2.connect(
        dbname="cine_match_db",
        user="postgres",
        password="Boka@1231",
        host="localhost",
        port="5432"
    )
    df = pd.read_sql("SELECT user_id, movie_id, rating FROM Ratings", conn)
    conn.close()
    return df

def train_svd_model():
    ratings_df = fetch_ratings()
    reader = Reader(rating_scale=(0, 5))
    data = Dataset.load_from_df(ratings_df[['user_id', 'movie_id', 'rating']], reader)
    trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)
    return algo

def predict_user_ratings(algo, user_id, movie_ids):
    preds = {}
    for movie_id in movie_ids:
        est = algo.predict(user_id, movie_id).est
        preds[movie_id] = est
    return preds
