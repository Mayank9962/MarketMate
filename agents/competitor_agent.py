from utils.scraper import search_serpapi
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def competitor_agent_node(state):
    """
    A LangGraph node representing the CompetitorAgent.
    It finds competitors based on the product line using web search.
    Preference order: Madhya Pradesh (India) → Other Indian states → Global fallback.
    """
    print(f"[CompetitorAgent] -> Searching for competitors...")
    product_line = state["product_line"]

    # Optional caller-provided location preference
    preferred_region = state.get("preferred_region", "Madhya Pradesh, India")
    
    # Register with MCP Server (if available)
    try:
        from mcp_server.server import MCPServer
        mcp_server = MCPServer()
        mcp_server.register_agent("competitor_agent", "analysis")
        mcp_server.log_analysis(product_line, "competitor_search", "started")
    except Exception as e:
        print(f"[CompetitorAgent] -> MCP registration failed: {e}")

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

    # Perform multiple location-biased searches and merge
    queries = [
        f"top {product_line} competitors in Madhya Pradesh India",
        f"top {product_line} companies in India",
        f"{product_line} leading Indian competitors",
        f"top competitors for {product_line}",  # global fallback
    ]

    aggregated_results = []
    for q in queries:
        try:
            res = search_serpapi(q)
            if res:
                aggregated_results.append({"query": q, "results": res})
        except Exception:
            continue

    if not aggregated_results:
        print("[CompetitorAgent] -> No search results found.")
        return {"competitors": []}

    prompt = PromptTemplate(
        template="""
You are selecting real company competitors for the product line "{product_line}" using the web search snippets below.

Selection rules (strict):
1) Prefer companies based in Madhya Pradesh, India first.
2) If fewer than 3 are found, add other Indian companies (any state).
3) Only if still fewer than 3, fill remaining slots with global competitors.
4) Output only company names, comma-separated. Do not include locations or descriptions.

Preferred region: {preferred_region}

Search bundles:
{search_results}

Return:
Competitors:
""",
        input_variables=["product_line", "search_results", "preferred_region"],
    )

    competitor_list_str = (
        llm.invoke(
            prompt.format(
                product_line=product_line,
                search_results=aggregated_results,
                preferred_region=preferred_region,
            )
        ).content.strip()
    )

    # Post-process to ensure we output only clean company names
    raw_lines = [line.strip() for line in competitor_list_str.splitlines() if line.strip()]
    tokens = []
    for line in raw_lines:
        if any(kw in line.lower() for kw in ["based on", "selection rules", "preferred region", "search bundles", "competitors:"]):
            continue
        # Split by commas to capture comma-separated names
        for part in line.split(","):
            name = part.strip().strip("-•*:\u2022")
            # Filter out non-company lines
            if not name:
                continue
            if ":" in name:
                continue
            if name.lower().startswith(("none ", "no company", "global competitors", "indian companies", "fashion companies")):
                continue
            tokens.append(name)

    # De-duplicate while preserving order
    seen = set()
    competitors = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            competitors.append(t)

    # Keep a reasonable number
    competitors = competitors[:10]

    print(f"[CompetitorAgent] -> Found competitors: {competitors}")
    
    # Log completion with MCP Server
    try:
        from mcp_server.server import MCPServer
        mcp_server = MCPServer()
        mcp_server.log_analysis(product_line, "competitor_search", f"completed - found {len(competitors)} competitors")
    except Exception as e:
        print(f"[CompetitorAgent] -> MCP logging failed: {e}")

    return {"competitors": competitors}