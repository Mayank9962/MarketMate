import os 
from serpapi import search 
 
def get_google_news_trends(query: str): 
    """ 
    Fetches trending news articles related to a query using SerpAPI. 
    """ 
    try: 
        results = search({ 
            "q": query, 
            "tbm": "news", 
            "api_key": os.getenv("SERPAPI_API_KEY") 
        }) 
         
        news_results = results.get("news_results", []) 
        if not news_results: 
            return [] 
             
        return news_results[:5] # Get top 5 news articles 
         
    except Exception as e: 
        print(f"Error fetching Google News: {e}") 
        return [] 