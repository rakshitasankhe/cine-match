CREATE TABLE IF NOT EXISTS Users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS Movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    release_year INT,
    description TEXT,
    duration INT,
    mood_tags TEXT,
    language VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Ratings (
    rating_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    movie_id INT REFERENCES Movies(movie_id) ON DELETE CASCADE,
    rating NUMERIC(2,1) CHECK (rating >= 0 AND rating <= 5),
    rating_date TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS UserMoodLogs (
    log_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES Users(user_id) ON DELETE CASCADE,
    mood VARCHAR(50),
    log_date TIMESTAMPTZ DEFAULT NOW()
);
