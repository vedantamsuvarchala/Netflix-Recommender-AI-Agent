import plotly.express as px
import pandas as pd
import streamlit as st

from agent import netflix_agent
from movie_details import get_movie_details
from tmdb import get_movie_poster, get_movie_trailer



def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

st.sidebar.title("🎬 Netflix AI")

st.sidebar.markdown("""
### Features
-  Analytics
- Movie Recommendation
- AI Agent
- Business Insights
                    
---
                    
Made with 🧠 using
Python . Streamlit . Scikit-learn 
""")

df = pd.read_csv("data/netflix_clean.csv")
movie_list = sorted(df["title"].dropna().unique())

total_titles = len(df)
total_movies = len(df[df["type"] == "Movie"])
total_shows = len(df[df["type"] == "TV Show"])


st.set_page_config(
    page_title="Netflix AI Analytics Agent",
    page_icon="🎬",
    layout="wide"
)

st.markdown(
    """
    <h1 style='text-align:center;color:#E50914;'>
     🎬 Netflix AI Analytics Agent
     </h1>
     <p style='text-align:center;color:white;font-size:18px;'>
     Discover insights, explore analytics, and get AI-powered movie recommendations.
     </p>
     """,
     unsafe_allow_html=True
)

tab1, tab2, tab3 = st.tabs([
    "📊 Dashboard",
    "🤖 AI Assistant",
    "🎬 Recommendation"
])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🎬 Total Titles", total_titles)

    with col2:
        st.metric("🎥 Movies", total_movies) 

    with col3:
        st.metric("📺 TV Shows", total_shows)

    genre_counts = (
        df["listed_in"]
        .str.split(", ")
        .explode()
        .value_counts()
        .head(10)
    )

    st.subheader("📊 Netflix Content Analytics Dashboard")

    fig = px.bar(
    x=genre_counts.values,
    y=genre_counts.index,
    orientation="h",
    labels={"x": "Number of Titles", "y": "Genre"},
    title="🎭 Top 10 Genres on Netflix",
    color=genre_counts.values,
    color_continuous_scale=[
        "#5B0000",
        "#8B0000",
        "#C00000",
        "#E50914",
        "#FF4D4D"
    ]
)

fig.update_coloraxes(showscale=False)

fig.update_layout(
    template="plotly",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=430,
    title_font_size=22,
    xaxis_title="Number of Titles",
    yaxis_title=""
)

type_counts = df["type"].value_counts()

fig2 = px.pie(
    values=type_counts.values,
    names=type_counts.index,
    title="🎬 Movies vs TV Shows",
    hole=0.55,
    color=type_counts.index,
    color_discrete_map={
        "Movie": "#E50914",
        "TV Show": "#4A90E2"
    }
)

fig2.update_layout(
    template="plotly",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=430,
    title_font_size=22,
    legend_title=""
)

fig2.update_traces(
    textinfo="percent+label",
    textfont_size=14,
    marker=dict(line=dict(color="#141414", width=2))
)


col_left, col_right = st.columns(2)

with col_left:
        st.plotly_chart(fig, width="stretch")

with col_right:
        st.plotly_chart(fig2, width="stretch")


st.subheader("🌍 Top 10 Content Producing Countries")

    
country_counts = (
    df["country"]
    .fillna("Unknown")
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)

    
)

fig3 = px.bar(
    x=country_counts.index,
    y=country_counts.values,
    labels={"x": "Country", "y": "Number of Titles"},
    title="Top 10 Countries by Netflix Content"
)

fig3.update_layout(
    template="plotly",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    height=500,
    xaxis_tickangle=-45
)

st.plotly_chart(fig3, use_container_width=True)

with tab2:
    query = st.text_input(
        "Ask an analytics question",
        placeholder="Example: top genres, movies, tv shows, countries"
    )

    ask = st.button("🚀 Ask AI")

    if ask:
        if query.strip():
            with st.spinner("🤖 AI is thinking..."):
                response = netflix_agent(query)

            st.markdown("### 📊 AI Response")
            st.info(response)

with tab3:

    selected_movie = st.selectbox(
        "🎬 Choose a Movie",
        movie_list
    )

    if st.button("✨ Discover Similar Movies"):

        with st.spinner("Finding similar movies..."):

            response = netflix_agent(f"recommend {selected_movie}")

        details = get_movie_details(selected_movie)

        if details:

            st.subheader("🎬 Selected Movie")

            poster = get_movie_poster(details["title"])
            
            col1, col2 = st.columns([1, 2])

            with col1:

                if poster:
                    st.image(poster, width="stretch")
                st.metric("⭐ Rating", details["rating"])
                st.metric("📅 Year", details["release_year"])
                st.metric("⏱ Duration", details["duration"])

            with col2:
                st.markdown(f"## 🎬 {details['title']}")
                st.write(f"**Genre:** {details['genre']}")
                st.write(f"**Director:** {details['director']}")
                st.write(f"**Cast:** {details['cast']}")
                st.write(details["description"])


            
            movie_name = details["title"].replace(" ", "+")
            trailer = get_movie_trailer(details["title"])

            st.markdown(
                f"""
<a href="https://www.imdb.com/find/?q={movie_name}" target="_blank">
    <button style="
        background:#E50914;
        color:white;
        padding:10px 20px;
        border:none;
        border-radius:8px;
        cursor:pointer;
        font-size:16px;">
        🎬 View on IMDb
    </button>
</a>
""",
    
            unsafe_allow_html=True,
            )

            if trailer:
                st.link_button("▶️ Watch Trailer", trailer)

            st.markdown("---")
            st.subheader("🎯 Similar Recommendations")

    for movie in response:
            st.markdown(f"""
<div style="
background:#202020;
padding:15px;
border-radius:10px;
margin-bottom:10px;
font-size:18px;
border-left:5px solid #E50914;">
🎬 {movie}
</div>
""", unsafe_allow_html=True)
            
st.subheader("🍿 Watch Now")

st.info(
    "Availability depends on your region. "
    "Click IMDb for streaming information and providers."
)
            
   

st.markdown("---")
st.caption("© 2026 Netflix AI Analytics Agent | Built by Suvarchala Vedantam 🚀")