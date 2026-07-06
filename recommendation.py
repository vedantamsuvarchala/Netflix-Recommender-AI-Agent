import pandas as pd
import joblib

df = pd.read_csv("data/netflix_clean.csv")

tfidf = joblib.load("models/tfidf.pkl")
tfidf_matrix = joblib.load("models/tfidf_matrix.pkl")

from sklearn.metrics.pairwise import cosine_similarity

similarity = cosine_similarity(tfidf_matrix)


def recommendation_tool(title):

    title = title.strip().lower()

    matches = df[df["title"].str.lower() == title]

    if matches.empty:
        return ["❌ Title not found. Please check the movie name."]

    idx = matches.index[0]

    scores = list(enumerate(similarity[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)

    recommendations = []

    for i in scores[1:6]:
        recommendations.append(df.iloc[i[0]]["title"])

    return recommendations