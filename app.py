import streamlit as st  # Import Streamlit for UI

from auth_utils import signup_user, login_user  # Import auth helper functions
from poster import get_poster_url                # Import TMDB poster fetcher
from loggers import log_user_mood, log_user_interaction  # Logging user activity
from collaborative_model import recommend_movies  # Movie recommendation engine

st.title("CineMatch Movie Recommendation System")  # Page title

# Sidebar lets user choose to Login or Signup
page = st.sidebar.selectbox("Choose Action", ["Login", "Signup"])

if page == "Signup":
    st.subheader("Create a new account")
    # Text inputs for signup details
    new_username = st.text_input("Username", key="signup_user")
    new_email = st.text_input("Email", key="signup_email")
    new_password = st.text_input("Password", type="password", key="signup_pass")
    confirm_password = st.text_input("Confirm Password", type="password", key="signup_pass_confirm")
    
    if st.button("Signup"):
        # Validate password confirmation and inputs
        if new_password != confirm_password:
            st.error("Passwords do not match")
        elif new_username == "" or new_email == "" or new_password == "":
            st.error("Please fill all fields")
        else:
            # Call signup_user, returns True if successful
            success = signup_user(new_username, new_email, new_password)
            if success:
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username or email already exists.")

elif page == "Login":
    st.subheader("Login to your account")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    
    if st.button("Login"):
        if username == "" or password == "":
            st.error("Please enter username and password")
        else:
            # Call login_user, returns True if login successful
            if login_user(username, password):
                st.success(f"Welcome back, {username}!")
                
                # After login, show mood and filter inputs
                mood = st.selectbox("How do you feel right now?", ['happy', 'sad', 'thrilling', 'romantic', 'scary', 'inspiring'])
                genre = st.text_input("Filter by genre (optional)")
                language = st.text_input("Filter by language (optional)")

                if st.button("Get Recommendations"):
                    # Log mood to DB
                    log_user_mood(username, mood)
                    # Get recommended movies as DataFrame
                    recs = recommend_movies(username, mood, genre, language)
                    if recs.empty:
                        st.warning("No movies found with those filters.")
                    else:
                        # Display each recommended movie
                        for _, row in recs.iterrows():
                            col1, col2 = st.columns([1, 4])  # Layout columns
                            with col1:
                                st.image(get_poster_url(row['title']), width=120)  # Show poster image
                            with col2:
                                st.markdown(f"**{row['title']}**")
                                st.markdown(f"Genre: {row['genre']} | Language: {row['language']}")
                                st.markdown(f"Mood Tags: {row['mood_tags']}")
                                st.markdown(f"⭐ {round(row['avg_rating'], 1)}")
                                # Button to simulate watching a movie and logging interaction
                                if st.button(f"🎬 Watch {row['title']}", key=row['movie_id']):
                                    log_user_interaction(username, row['movie_id'])
                                    st.success("Logged your interaction!")
            else:
                st.error("Invalid username or password")
