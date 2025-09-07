from mcp_server.memory_store import MemoryStore 
from datetime import date 
 
def memory_agent_node(state: dict, memory_store: MemoryStore): 
    """ 
    A LangGraph node representing the MemoryAgent. 
    It interacts with the MCP-style memory store to retrieve and store 
data. 
    """ 
    print("[MemoryAgent] -> Interacting with the memory store...") 
    
    try:
        product_line = state.get("product_line") 
         
        # Attempt to retrieve historical data 
        historical_data = memory_store.get_data(product_line) 
        if historical_data: 
            print(f"[MemoryAgent] -> Found historical data from {historical_data['date']}.") 
            state["historical_data"] = historical_data 
        else:
            print("[MemoryAgent] -> No historical data found for this product line.")

        # Store the current state for future comparison 
        current_data = { 
            "date": date.today().strftime("%Y-%m-%d"), 
            "competitors": state.get("competitors", []), 
            "reviews": state.get("reviews", {}), 
            "trends": state.get("trends", []) 
        } 
        memory_store.store_data(product_line, current_data) 
        print("[MemoryAgent] -> Stored current market data for future use.") 
         
        return state
        
    except Exception as e:
        print(f"[MemoryAgent] -> Error in memory operations: {e}")
        # Continue without memory operations if they fail
        return state