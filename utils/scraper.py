import os 
import requests 
from serpapi import search 
 
def search_serpapi(query: str): 
    """ 
    Performs a web search using SerpAPI. 
    Returns the search results as a formatted string. 
    """ 
    try: 
        results = search({"q": query, "api_key": os.getenv("SERPAPI_API_KEY")}) 
         
        organic_results = results.get("organic_results", []) 
         
        if not organic_results: 
            return "No results found." 
             
        formatted_results = [] 
        for r in organic_results[:5]: # Get top 5 results 
            title = r.get("title", "") 
            snippet = r.get("snippet", "") 
            link = r.get("link", "") 
            formatted_results.append(f"Title: {title}\nSnippet: {snippet}\nLink: {link}\n") 
             
        return "\n---\n".join(formatted_results) 
         
    except Exception as e: 
        print(f"Error with SerpAPI: {e}") 
        return "No results found." 
 
def scrape_reviews(query: str): 
    """ 
    Simulates scraping reviews from a web search. 
    In a real scenario, this would use a full-fledged scraper like 
BeautifulSoup. 
    For this example, we'll return mock data. 
    """ 
    print(f"Simulating scraping for: {query}") 
    mock_reviews = [ 
        "These brake pads are excellent! Great stopping power and no noise.", 
        "They wore out faster than I expected, but the initial performance was good.", 
        "Easy to install and feel very responsive. Highly recommend.", 
        "The packaging was damaged and one pad was chipped.", 
        "A bit pricey, but the quality is top-notch. You get what you pay for." 
    ] 
    return mock_reviews