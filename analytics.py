import pandas as pd

df = pd.read_csv("data/netflix_clean.csv", encoding="utf-8")
print(df.head())

def dataset_tool(query):

    query = query.lower()

    if "top genres" in query:
        return (
            df["listed_in"]
            .str.split(", ")
            .explode()
            .value_counts()
            .head(10)
        )
    elif "movies" in query:
        return df[df["type"] == "Movie"].shape[0]

    elif "tv shows" in query:
        return df[df["type"] == "TV Show"].shape[0]

    elif "countries" in query:
        return (
            df["country"]
            .dropna()
            .str.split(", ")
            .explode()
            .value_counts()
            .head(10)
        )

    else:
        return "Sorry, I don't understand that query."


def analytics_summary(question):

    result = dataset_tool(question)

    report = f"""
==============================
      NETFLIX ANALYTICS REPORT
==============================

Query:
{question}

--------------------------------
Result
--------------------------------
{result}

--------------------------------
Business Insight
--------------------------------
The above results highlight the most significant patterns in the Netflix dataset.
These insights can help Netflix understand customer preferences,
optimize content acquisition, and improve recommendation strategies.
"""

    return report
 
        

  