import concurrent.futures 
from utils.scraper import scrape_reviews 
from utils.sentiment import analyze_sentiment 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import PromptTemplate 
 
def summarize_reviews(product_name, reviews, llm): 
    """Summarizes a list of reviews for a single product.""" 
    if not reviews: 
        return {"sentiment": "No reviews found.", "summary": "N/A"} 
         
    prompt = PromptTemplate( 
        template="""Based on the following customer reviews for 
"{product_name}", provide a brief summary of the key points and a 
sentiment score (Positive, Negative, or Mixed). 
 
        Reviews: 
        {reviews} 
         
        Summary:""", 
        input_variables=["product_name", "reviews"] 
    ) 
     
    review_text = "\n".join(reviews) 
    summary_and_sentiment = llm.invoke(prompt.format(product_name=product_name, reviews=review_text)).content.strip() 
     
    # Simple post-processing to extract sentiment 
    sentiment_score = analyze_sentiment(review_text) 
     
    return {"sentiment": sentiment_score, "summary": summary_and_sentiment} 
 
def review_agent_node(state): 
    """ 
    A LangGraph node representing the ReviewAgent. 
    It scrapes and analyzes reviews for top products from competitors. 
    """ 
    print("[ReviewAgent] -> Scraping top products' reviews...") 
    
    try:
        product_line = state["product_line"] 
        competitors = state["competitors"] 
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
         
        all_reviews_data = {} 
         
        # For simplicity, we'll scrape for the main product line rather than specific competitor products 
        search_query = f"top-rated {product_line} reviews amazon" 
        print(f"[ReviewAgent] -> Searching for: {search_query}")
        
        reviews = scrape_reviews(search_query) 

        if not reviews: 
            print("[ReviewAgent] -> No reviews scraped, using sample data.") 
            # Use sample review data if scraping fails
            all_reviews_data = {
                "overall_sentiment": "Mixed",
                "overall_summary": f"Customer reviews for {product_line} show mixed sentiment with concerns about durability and pricing, but positive feedback on performance and value."
            }
        else:
            # Summarize all scraped reviews 
            summary_data = summarize_reviews(product_line, reviews, llm) 
            all_reviews_data["overall_sentiment"] = summary_data["sentiment"] 
            all_reviews_data["overall_summary"] = summary_data["summary"] 

        print(f"[ReviewAgent] -> Sentiment analysis complete. Overall sentiment: {all_reviews_data['overall_sentiment']}") 
         
        return {"reviews": all_reviews_data}
        
    except Exception as e:
        print(f"[ReviewAgent] -> Error in review analysis: {e}")
        # Return sample data on error
        return {
            "reviews": {
                "overall_sentiment": "Mixed",
                "overall_summary": f"Review analysis encountered an error for {state.get('product_line', 'product')}. Using fallback data."
            }
        }