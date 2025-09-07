# MarketMate AI

MarketMate AI is a modular, multi-agent system for market analysis, competitor research, sentiment analysis, and actionable business recommendations. It uses LangGraph for agent orchestration and MCP-style memory for historical comparison.

## Features
- Competitor discovery via web search
- Review scraping and sentiment analysis
- Trend extraction from social media/news
- PDF report generation
- Optional voice summary (TTS)
- Historical data comparison

## Setup
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **API Keys Configuration:**
   
   The API keys are already configured in `config.py` with the provided keys:
   - Google Gemini API Key: ✅ Configured
   - SerpAPI Key: ✅ Configured
   
   If you need to change the API keys, edit the `config.py` file or set environment variables:
   ```bash
   export GOOGLE_API_KEY="your-new-google-api-key"
   export SERPAPI_API_KEY="your-new-serpapi-key"
   ```
   
4. **Test the API keys:**
   ```bash
   python test_api_keys.py
   ```

## Usage
Run the main script:
```bash
python main.py
```
You will be prompted for a product line (e.g., `motorcycle brake pads`).

## Sample Run
```
Enter the product line to analyze (e.g.,'motorcycle brake pads'): motorcycle brake pads

--- Starting MarketMate AI Analysis ---
[InputAgent] -> Received product line: motorcycle brake pads
[CompetitorAgent] -> Found competitors: Bosch, TVS, Brembo
[ReviewAgent] -> Scraped 120 reviews. Sentiment: Positive
[TrendAgent] -> Top trends: "ABS brakes", "eco-friendly pads"
[MemoryAgent] -> Compared with last week. Trends up: "eco-friendly pads"
[AdvisorAgent] -> Recommendations: Focus on eco-friendly marketing, highlight ABS compatibility.
--- Analysis Complete ---

--- Final Report Summary ---
Product Line: motorcycle brake pads
Report saved to: market_report_2024-06-01.pdf
----------------------------
[TTS] -> Starting voice summary...
```

## Output
- PDF report in the current directory
- Console summary
- Optional voice summary (if TTS enabled)

## Notes
- For best results, use valid API keys.
- All data is stored in the `data/` directory for historical comparison. 