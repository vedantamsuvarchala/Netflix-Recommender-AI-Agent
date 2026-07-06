import streamlit as st

from agent import netflix_agent

st.set_page_config(
    page_title="Netflix AI Analytics Agent",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Netflix AI Analytics Agent")

query = st.text_input("Ask a question or type: recommend <movie name>")

if st.button("Ask"):

    if query.strip():

        response = netflix_agent(query)

        if isinstance(response, list):
            st.subheader("🎯 Recommendations")
            for movie in response:
                st.write("✅", movie)
        else:
            st.text(response)