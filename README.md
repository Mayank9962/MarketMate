## MarketMate AI

Voice‑enabled market intelligence dashboard built with Streamlit. Discover competitors and trends, generate strategic recommendations with predictive analytics, and export polished PDF reports—plus rich interactive visualizations.

### ✨ Features
- **Voice I/O**: Speak product lines; optional text‑to‑speech summaries
- **Competitor Discovery**: Region‑aware search (MP → India → Global)
- **Trend Mining**: News‑driven market trends with concise bullets
- **Advisor Reports**: Actionable strategy (exec summary, roadmap, risks, KPIs)
- **Predictive Analytics**: Sales, growth, pricing, seasonal patterns
- **Beautiful Visuals**: Market share, sentiment, radar, geo heatmaps, and more
- **One‑click PDF Export**: Branded, ready‑to‑share reports

### 🧱 Tech Stack
- Python, Streamlit, Plotly
- LangChain + Google Generative AI (Gemini)
- SERPAPI (search), SpeechRecognition, pyttsx3

### 📦 Quick Start
1) Clone and enter the project
```bash
git clone https://github.com/your-username/marketmate_ai.git
cd marketmate_ai
```

2) Create a virtual environment (recommended)
```bash
python -m venv .venv
# Windows PowerShell
. .venv/Scripts/Activate.ps1
```

3) Install dependencies
```bash
pip install -r requirements.txt
```

4) Set environment variables
Create a `.env` file in the project root:
```bash
GOOGLE_API_KEY=your_google_generative_ai_key
SERPAPI_API_KEY=your_serpapi_key
```

5) Run the dashboard
```bash
streamlit run dashboard_voice.py
```

### 🗺️ How To Use
1) Enter or speak a product line (e.g., "smartphone accessories", "motorcycle brake pads").
2) Choose the analysis type and preferred region from the sidebar.
3) Click "Run Advanced Analysis" to generate competitors, trends, and recommendations.
4) Explore interactive charts; download the PDF report when ready.
5) Use "Quick Visualize" for fast visual insights without a full run.

### 📁 Project Structure (key files)
```
marketmate_ai/
  dashboard_voice.py        # Streamlit app (UI + workflow)
  graph/market_graph.py     # Orchestration over agents
  agents/                   # Modular agents
    competitor_agent.py     # Finds competitors (SERPAPI + Gemini)
    trend_agent.py          # Extracts market trends (News + Gemini)
    advisor_agent.py        # Strategic advisory + PDF + predictive
  utils/                    # Visuals, scraping, analytics helpers
  data/                     # Saved visualization JSON & samples
  reports/                  # Generated PDF reports
  config.py                 # Loads API keys from .env
  requirements.txt
```

### 🔐 Security Notes
- Do not commit real API keys. Use `.env` and keep it out of version control.
- If you fork this repo, rotate any keys that may have been exposed previously.

### 🛠 Troubleshooting
- Streamlit doesn’t load or errors on syntax: pull latest and re‑run.
- Empty outputs: ensure valid `GOOGLE_API_KEY` and `SERPAPI_API_KEY` are set.
- Slow first run: models and caches initialize; subsequent runs are faster.
- Microphone not detected: check OS permissions and default input device.

### 🗓 Roadmap
- Offline caching for repeat queries
- Additional data sources (social, pricing APIs)
- Export to PPTX and Excel

### 🤝 Contributing
PRs welcome! Please open an issue to discuss substantial changes.

### 📄 License
MIT


