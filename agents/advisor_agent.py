from utils.report_generator import generate_pdf_report, generate_voice_summary 
from utils.visualization_simple import SimpleVisualizer
from utils.predictive_analytics_simple import SimplePredictiveAnalytics
from langchain_google_genai import ChatGoogleGenerativeAI 
from langchain_core.prompts import PromptTemplate 
from datetime import date 
import json
import os

def advisor_agent_node(state): 
    """ 
    A LangGraph node representing the AdvisorAgent. 
    It synthesizes insights and generates actionable recommendations with predictive analytics.
    """ 
    print("[AdvisorAgent] -> Synthesizing insights and generating recommendations...") 
    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash") 
        
        # Initialize visualization and predictive analytics
        visualizer = SimpleVisualizer()
        predictor = SimplePredictiveAnalytics()
         
        # Combine data from all agents 
        product_line = state.get("product_line") 
        competitors = state.get("competitors", []) 
        reviews = state.get("reviews", {}) 
        trends = state.get("trends", []) 
        historical_data = state.get("historical_data", {}) 

        # Generate predictive analytics
        print("[AdvisorAgent] -> Generating predictive analytics...")
        forecast_data = predictor.generate_comprehensive_forecast(product_line, competitors)
        
        # Generate visualizations
        print("[AdvisorAgent] -> Creating advanced visualizations...")
        visualizations = {}
        
        if competitors:
            visualizations['market_share_pie'] = visualizer.create_market_share_pie(competitors)
            visualizations['competitor_radar'] = visualizer.create_competitor_radar(competitors)
        
        visualizations['sentiment_trend'] = visualizer.create_sentiment_trend_line(None)
        visualizations['price_histogram'] = visualizer.create_price_histogram()
        visualizations['geographic_heatmap'] = visualizer.create_geographic_heatmap()

        prompt_template = """ 
        You are a senior business advisor with expertise in market analysis and predictive analytics. 
        Your task is to provide comprehensive, actionable recommendations based on the following data:

        --- 
        **Product Line:** {product_line} 
         
        **Competitors:** {competitors}

        **Customer Sentiment Summary:** 
        {review_summary}

        **Current Market Trends:** 
        {trends}

        **Historical Context (if available):** 
        {historical_context}

        **Predictive Analytics Insights:**
        {predictive_insights}

        --- 

        Based on this comprehensive analysis, provide:
        1. **Executive Summary** (2-3 sentences)
        2. **Strategic Recommendations** (5-7 bullet points)
        3. **Risk Assessment** (3-4 key risks)
        4. **Implementation Timeline** (Next 3, 6, 12 months)
        5. **Success Metrics** (KPIs to track)

        Focus on actionable insights that drive business growth and competitive advantage.
        """ 

        historical_context_str = "No historical data available for comparison." 
        if historical_data: 
            historical_context_str = f"Last week's trends: {historical_data.get('trends', 'N/A')}\nLast week's sentiment: {historical_data.get('reviews', {}).get('overall_sentiment', 'N/A')}" 
        
        # Format predictive insights
        predictive_insights = "No predictive analytics available."
        if forecast_data:
            predictive_insights = f"""
            **Sales Forecast:** {len(forecast_data.get('sales_forecast', []))} months ahead
            **Market Growth:** {len(forecast_data.get('market_growth', []))} years projection
            **Competitor Strategies:** {len(forecast_data.get('competitor_strategies', []))} competitors analyzed
            **Price Trends:** {len(forecast_data.get('price_trends', []))} months price prediction
            **Seasonal Analysis:** Complete seasonal demand patterns
            """
         
        prompt = PromptTemplate( 
            template=prompt_template, 
            input_variables=["product_line", "competitors", 
    "review_summary", "trends", "historical_context", "predictive_insights"] 
        ) 
         
        recommendations = llm.invoke(prompt.format( 
            product_line=product_line, 
            competitors=", ".join(competitors), 
            review_summary=reviews.get("overall_summary", "No review data available."), 
            trends="\n".join(trends), 
            historical_context=historical_context_str,
            predictive_insights=predictive_insights
        )).content.strip() 
         
        print("[AdvisorAgent] -> Generating final PDF report...") 
         
        report_data = { 
            "title": f"Advanced Market Analysis Report for {product_line}", 
            "date": date.today().strftime("%Y-%m-%d"), 
            "product_line": product_line, 
            "competitors": competitors, 
            "reviews": reviews, 
            "trends": trends, 
            "recommendations": recommendations, 
            "historical_data": historical_data,
            "predictive_analytics": forecast_data,
            "visualizations": visualizations
        } 
         
        # Generate the PDF report 
        report_file = generate_pdf_report(report_data) 
         
        print(f"[AdvisorAgent] -> Report saved to {report_file}") 
         
        # Save visualization data for dashboard
        try:
            viz_data = {
                'product_line': product_line,
                'competitors': competitors,
                'forecast_data': forecast_data,
                'visualizations_available': list(visualizations.keys())
            }
            
            # Save to data directory
            os.makedirs('data', exist_ok=True)
            viz_file = f"data/{product_line.replace(' ', '_').replace('/', '_')}_visualization_data.json"
            with open(viz_file, 'w') as f:
                json.dump(viz_data, f, indent=2, default=str)
            
            print(f"[AdvisorAgent] -> Visualization data saved to {viz_file}")
        except Exception as e:
            print(f"[AdvisorAgent] -> Error saving visualization data: {e}")

        # Update state with recommendations and report file path (always)
        state["recommendations"] = recommendations
        state["report_file"] = report_file
        state["predictive_analytics"] = forecast_data
        state["visualizations"] = visualizations

        return state
        
    except Exception as e:
        print(f"[AdvisorAgent] -> Error in advisor analysis: {e}")
        # Return basic recommendations on error
        product_line = state.get("product_line", "product")
        competitors = state.get("competitors", [])
        
        basic_recommendations = f"""
        Based on the analysis of {product_line}, here are key recommendations:
        
        1. **Market Analysis**: Focus on the identified competitors: {', '.join(competitors) if competitors else 'No competitors identified'}
        2. **Strategic Positioning**: Develop unique value propositions to differentiate from competitors
        3. **Customer Focus**: Implement customer feedback mechanisms to improve product quality
        4. **Market Expansion**: Explore new market segments and geographic regions
        5. **Technology Integration**: Leverage technology to enhance product offerings
        
        Note: This is a basic analysis due to technical limitations. For comprehensive insights, please ensure all data sources are properly configured.
        """
        
        state["recommendations"] = basic_recommendations
        state["report_file"] = None
        state["predictive_analytics"] = {}
        state["visualizations"] = {}
        
        return state