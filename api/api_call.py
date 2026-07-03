import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OMDB_API_KEY")


def get_movie_by_name(name):
    """Look up a movie by title on OMDb. Returns a dict, or None on failure."""
    if not API_KEY:
        return None
    try:
        response = requests.get(
            "https://www.omdbapi.com/",
            params={"apikey": API_KEY, "t": name},
            timeout=5
        )
        data = response.json()
    except requests.RequestException:
        return None

    if data.get("Response") == "False":
        return None
    return data