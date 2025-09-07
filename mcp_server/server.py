"""
This module represents a simple, class-based MCP server.
In a production-level distributed system, this would be a full-fledged
API or service for managing memory state.
For this project, it acts as a centralized access point for the MemoryStore.
"""

from mcp_server.memory_store import MemoryStore
from datetime import datetime

class MCPServer:
    """
    A lightweight, class-based server to manage the MemoryStore.
    Agents can "connect" to this server to get and set shared state.
    This acts as the central coordinator for all agent interactions.
    """
    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one instance of the server exists."""
        if cls._instance is None:
            cls._instance = super(MCPServer, cls).__new__(cls)
            cls._instance.memory_store = MemoryStore()
            cls._instance.agent_connections = {}
            cls._instance.analysis_history = []
            print("[MCPServer] -> Server initialized (Singleton)")
        return cls._instance

    def get_memory_store(self):
        """Returns the single instance of the MemoryStore."""
        return self.memory_store

    def register_agent(self, agent_name: str, agent_type: str):
        """Register an agent with the MCP server."""
        self.agent_connections[agent_name] = {
            "type": agent_type,
            "connected_at": datetime.now().isoformat(),
            "status": "active"
        }
        print(f"[MCPServer] -> Agent '{agent_name}' ({agent_type}) registered")

    def log_analysis(self, product_line: str, analysis_type: str, status: str):
        """Log analysis activities for monitoring."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "product_line": product_line,
            "analysis_type": analysis_type,
            "status": status
        }
        self.analysis_history.append(log_entry)
        print(f"[MCPServer] -> Analysis logged: {product_line} - {analysis_type} - {status}")

    def get_server_status(self):
        """Get current server status and statistics."""
        return {
            "connected_agents": len(self.agent_connections),
            "total_analyses": len(self.analysis_history),
            "memory_store_active": self.memory_store is not None,
            "agent_connections": self.agent_connections,
            "recent_analyses": self.analysis_history[-5:] if self.analysis_history else []
        }

# Example usage (not used in main.py, but shows the design pattern)
if __name__ == "__main__":
    # Agent 1 connects to the server
    server1 = MCPServer()
    memory_store1 = server1.get_memory_store()
    
    # Agent 2 connects to the server
    server2 = MCPServer()
    memory_store2 = server2.get_memory_store()
    
    # Both agents access the same MemoryStore instance
    print(f"Are memory stores the same instance? {memory_store1 is memory_store2}")
    
    memory_store1.store_data("example_product", {"data": "test"})
    retrieved_data = memory_store2.get_data("example_product")
    print(f"Retrieved data: {retrieved_data}")