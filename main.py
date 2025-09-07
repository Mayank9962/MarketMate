import os 
import datetime 
import config  # Import config to load API keys
from graph.market_graph import MarketGraph 
from mcp_server.server import MCPServer 
 
def main(): 
    """ 
    Main entry point for the MarketMate AI application. 
    Orchestrates the LangGraph workflow and handles user interaction. 
    """ 
    if not os.getenv("GOOGLE_API_KEY"): 
        raise ValueError("GOOGLE_API_KEY environment variable not set.") 
     
    if not os.getenv("SERPAPI_API_KEY"): 
        raise ValueError("SERPAPI_API_KEY environment variable not set.") 
 
    product_line = input("Enter the product line to analyze (e.g.,'motorcycle brake pads'): ") 
     
    # Initialize MCP Server and get memory store
    mcp_server = MCPServer()
    memory_store = mcp_server.get_memory_store() 
     
    # Initialize the LangGraph workflow 
    graph = MarketGraph(memory_store) 
     
    # Define the initial state for the graph 
    initial_state = { 
        "product_line": product_line, 
        "competitors": [], 
        "reviews": {}, 
        "trends": {}, 
        "recommendations": None, 
        "report_file": None, 
        "historical_data": None 
    } 
     
    # Run the graph 
    print("\n--- Starting MarketMate AI Analysis ---") 
    final_state = graph.run_graph(initial_state) 
    print("--- Analysis Complete ---") 
     
    # Final output summary 
    print("\n--- Final Report Summary ---") 
    print(f"Product Line: {final_state['product_line']}") 
    print(f"Report saved to: {final_state['report_file']}") 
    print("----------------------------") 
     
    # Optional voice summary 
    try: 
        from utils.report_generator import generate_voice_summary 
        generate_voice_summary(final_state['recommendations']) 
    except Exception as e: 
        print(f"Voice summary failed: {e}") 
 
if __name__ == "__main__": 
    main()