import requests

TMDB_API_KEY = "your_tmdb_api_key"

def get_poster_url(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://i.imgur.com/Q7bZL1V.png"  # fallback image

    data = response.json()
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w200{poster_path}"
    return "https://i.imgur.com/Q7bZL1V.png"
