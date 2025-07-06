import psycopg2  # PostgreSQL DB adapter
import bcrypt   # Password hashing library

# Database connection parameters (update with your own)
DB_PARAMS = {
    "dbname": "cine_match_db",
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()                      # Generate random salt
    hashed = bcrypt.hashpw(password.encode(), salt)  # Hash password with salt
    return hashed.decode()                        # Return string form

def verify_password(password: str, hashed: str) -> bool:
    # Check if plain password matches hashed password
    return bcrypt.checkpw(password.encode(), hashed.encode())

def signup_user(username: str, email: str, password: str) -> bool:
    hashed_pw = hash_password(password)          # Hash password before saving
    try:
        conn = psycopg2.connect(**DB_PARAMS)    # Connect to DB
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)
        """, (username, email, hashed_pw))     # Insert new user with hashed password
        conn.commit()
        cur.close()
        conn.close()
        return True
    except psycopg2.errors.UniqueViolation:
        # User/email already exists, return False
        return False
    except Exception as e:
        print("Signup error:", e)
        return False

def login_user(username: str, password: str) -> bool:
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        cur.execute("SELECT password FROM Users WHERE username = %s", (username,))
        result = cur.fetchone()  # Fetch stored password hash
        cur.close()
        conn.close()
        if result:
            stored_hash = result[0]
            return verify_password(password, stored_hash)  # Check password match
        else:
            return False
    except Exception as e:
        print("Login error:", e)
        return False
