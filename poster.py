import requests

TMDB_API_KEY = "your_tmdb_api_key"

def get_poster_url(title):
    # Call TMDB search API with movie title
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    if response.status_code != 200:
        # Return fallback image if API fails
        return "https://i.imgur.com/Q7bZL1V.png"
    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            # Build full image URL from TMDB path
            return f"https://image.tmdb.org/t/p/w200{poster_path}"
    # Return fallback if no poster found
    return "https://i.imgur.com/Q7bZL1V.png"
