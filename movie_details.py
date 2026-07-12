import pandas as pd

df = pd.read_csv("data/netflix_clean.csv")


def get_movie_details(title):
    movie = df[df["title"].str.lower() == title.lower()]

    if movie.empty:
        return None

    movie = movie.iloc[0]

    return {
        "title": movie["title"],
        "type": movie["type"],
        "director": movie["director"],
        "cast": movie["cast"],
        "country": movie["country"],
        "release_year": movie["release_year"],
        "rating": movie["rating"],
        "duration": movie["duration"],
        "genre": movie["listed_in"],
        "description": movie["description"]
    }