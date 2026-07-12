import os
import requests
from dotenv import load_dotenv
from functools import lru_cache


load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

@lru_cache(maxsize=100)
def get_movie_poster(movie_name):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    data = response.json()

    if not data["results"]:
        return None

    poster_path = data["results"][0].get("poster_path")

    if not poster_path:
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"


@lru_cache(maxsize=100)
def get_movie_trailer(movie_name):

    url = "https://api.themoviedb.org/3/search/movie"

    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    results = response.json()["results"]

    if not results:
        return None

    movie_id = results[0]["id"]

    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos"

    try:
        response = requests.get(
            url,
            params={"api_key": API_KEY},
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return None

    videos = response.json()["results"]

    for video in videos:
        if video["site"] == "YouTube" and video["type"] == "Trailer":
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None