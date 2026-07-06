from analytics import analytics_summary
from recommendation import recommendation_tool

def netflix_agent(user_query):

    query = user_query.lower()

    if "recommend" in query:
        
        title = user_query.replace("recommend", "").strip()

        return recommendation_tool(title)
    
    else:
        return analytics_summary(user_query)