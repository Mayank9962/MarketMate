import json 
import os 
from datetime import date 
 
class MemoryStore: 
    """ 
    An MCP-style memory store for persistent agent data. 
    Uses a simple file-based approach for demonstration. 
    """ 
    def __init__(self, data_dir="data"): 
        self.data_dir = data_dir 
        if not os.path.exists(self.data_dir): 
            os.makedirs(self.data_dir) 
 
    def _get_filepath(self, product_line: str): 
        """Generates a safe filename from the product line.""" 
        import re
        # Remove or replace invalid characters for filenames
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', product_line)
        safe_name = safe_name.replace(" ", "_").lower()
        # Limit length to avoid filesystem issues
        if len(safe_name) > 100:
            safe_name = safe_name[:100]
        return os.path.join(self.data_dir, f"{safe_name}.json") 
 
    def store_data(self, product_line: str, data: dict): 
        """Stores data related to a product line.""" 
        filepath = self._get_filepath(product_line) 
        with open(filepath, 'w') as f: 
            json.dump(data, f, indent=4) 
             
    def get_data(self, product_line: str): 
        """Retrieves data for a product line, if it exists.""" 
        filepath = self._get_filepath(product_line) 
        if os.path.exists(filepath): 
            with open(filepath, 'r') as f: 
                return json.load(f) 
        return None