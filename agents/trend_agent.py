from utils.social import get_google_news_trends 
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import PromptTemplate 
 
def trend_agent_node(state): 
    """ 
    A LangGraph node representing the TrendAgent. 
    It extracts latest market trends from Google News. 
    """ 
    print("[TrendAgent] -> Extracting trends from social media and news...") 
    
    try:
        product_line = state["product_line"] 
         
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
         
        # Use utility to get trending news articles 
        news_articles = get_google_news_trends(product_line) 
         
        if not news_articles: 
            print("[TrendAgent] -> No trends found, using sample data.") 
            # Use sample trend data if news extraction fails
            trends = [
                f"Growing demand for {product_line} in digital marketplaces",
                f"Innovation in {product_line} technology and features",
                f"Consumer preference shifting towards sustainable {product_line}",
                f"Market consolidation in {product_line} sector",
                f"Emerging trends in {product_line} pricing strategies"
            ]
        else:
            prompt = PromptTemplate( 
                template="""Based on the following news headlines, summarize 
    the key market trends, technological innovations, or consumer shifts 
    related to "{product_line}". 
            Return a bullet-point list of the top 3-5 trends. 

            News headlines: 
            {headlines} 
             
            Trends:""", 
                input_variables=["product_line", "headlines"] 
            ) 
             
            headlines_text = "\n".join([article["title"] for article in news_articles]) 
            trends_list_str = llm.invoke(prompt.format(product_line=product_line, headlines=headlines_text)).content.strip() 

            # Normalize into clean bullet points without numeric prefixes or extra text
            raw_lines = [line.strip() for line in trends_list_str.split("\n") if line.strip()]
            trends = []
            for line in raw_lines:
                # Remove leading bullets or numbers
                line = line.lstrip("-•* ")
                if line[:2].isdigit() and line[2:].lstrip(".) "):
                    # handle formats like '1. Trend' or '2) Trend'
                    idx = 0
                    while idx < len(line) and line[idx].isdigit():
                        idx += 1
                    line = line[idx:].lstrip(".) ")
                # Drop meta-lines
                if any(kw in line.lower() for kw in ["news headlines", "trends:", "summary:"]):
                    continue
                if line:
                    trends.append(line)
            trends = trends[:5]

        print(f"[TrendAgent] -> Found key trends: {trends}") 
         
        return {"trends": trends}
        
    except Exception as e:
        print(f"[TrendAgent] -> Error in trend analysis: {e}")
        # Return sample data on error
        return {
            "trends": [
                f"Market growth in {state.get('product_line', 'product')} sector",
                f"Technology innovation driving {state.get('product_line', 'product')} adoption",
                f"Consumer behavior shifts in {state.get('product_line', 'product')} preferences"
            ]
        }