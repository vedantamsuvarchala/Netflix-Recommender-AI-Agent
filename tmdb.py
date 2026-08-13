import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

BASE_URL = "https://api.themoviedb.org/3"


@st.cache_data(ttl=3600)
def search_movie(movie_name):
    try:
        response = requests.get(
            f"{BASE_URL}/search/movie",
            params={
                "api_key": API_KEY,
                "query": movie_name,
                "language": "en-US"
            },
            timeout=15
        )

        response.raise_for_status()
        results = response.json().get("results", [])

        if not results:
            return None

        # Prefer exact title match
        for movie in results:
            if movie.get("title", "").lower() == movie_name.lower():
                return movie

        return results[0]

    except requests.exceptions.RequestException:
        return None


@st.cache_data(ttl=3600)
def get_movie_poster(movie_name):

    movie = search_movie(movie_name)

    if not movie:
        return None

    poster_path = movie.get("poster_path")

    if not poster_path:
        return None

    return f"https://image.tmdb.org/t/p/w500{poster_path}"


@st.cache_data(ttl=3600)
def get_movie_trailer(movie_name):

    movie = search_movie(movie_name)

    if not movie:
        return None

    movie_id = movie.get("id")

    if not movie_id:
        return None

    try:
        response = requests.get(
            f"{BASE_URL}/movie/{movie_id}/videos",
            params={
                "api_key": API_KEY,
                "language": "en-US"
            },
            timeout=15
        )

        response.raise_for_status()

        videos = response.json().get("results", [])

        # First preference: official YouTube trailer
        for video in videos:
            if (
                video.get("site") == "YouTube"
                and video.get("type") == "Trailer"
                and video.get("key")
            ):
                return f"https://www.youtube.com/watch?v={video['key']}"

        # Fallback: any YouTube video
        for video in videos:
            if (
                video.get("site") == "YouTube"
                and video.get("key")
            ):
                return f"https://www.youtube.com/watch?v={video['key']}"

        return None

    except requests.exceptions.RequestException:
        return None