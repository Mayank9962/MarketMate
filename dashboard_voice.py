import streamlit as st
import os
import json
from datetime import datetime
import config
from graph.market_graph import MarketGraph
from mcp_server.server import MCPServer
import speech_recognition as sr
import pyttsx3
import threading
import queue
import time
import base64
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import plotly.graph_objects as go


st.set_page_config(
    page_title="MarketMate AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .voice-button {
        background-color: #28a745;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 25px;
        cursor: pointer;
        font-size: 16px;
        margin: 5px;
    }
    .voice-button:hover {
        background-color: #218838;
    }
    .voice-button:active {
        background-color: #1e7e34;
    }
</style>
""", unsafe_allow_html=True)

#speech recognition and text-to-speech
def init_voice():
    """Initialize voice components"""
    try:
        recognizer = sr.Recognizer()
        engine = pyttsx3.init()
        return recognizer, engine
    except Exception as e:
        st.error(f"Voice initialization failed: {e}")
        return None, None

def listen_for_speech(recognizer):
    """Listen for voice input"""
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            st.success(f"🎤 Heard: {text}")
            return text
    except sr.WaitTimeoutError:
        st.error("⏰ No speech detected within timeout")
        return None
    except sr.UnknownValueError:
        st.error("❓ Could not understand audio")
        return None
    except Exception as e:
        st.error(f"🎤 Error: {e}")
        return None

def speak_text(engine, text):
    """Convert text to speech"""
    try:
        engine.say(text)
        engine.runAndWait()
        st.success("🔊 Voice output completed")
    except Exception as e:
        st.error(f"🔊 Voice output error: {e}")

def create_pdf_report(analysis_data, product_line):
    """Create a PDF report from analysis data"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph(f"MarketMate AI Analysis Report", title_style))
    story.append(Paragraph(f"Product Line: {product_line}", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # Date
    story.append(Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Competitors Section
    if analysis_data.get("competitors"):
        story.append(Paragraph("🏢 Competitors Found", styles['Heading2']))
        competitor_data = []
        for i, competitor in enumerate(analysis_data["competitors"], 1):
            competitor_data.append([f"{i}.", competitor])
        
        if competitor_data:
            competitor_table = Table(competitor_data, colWidths=[0.5*inch, 4*inch])
            competitor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(competitor_table)
        story.append(Spacer(1, 20))
    
    # Trends Section
    if analysis_data.get("trends"):
        story.append(Paragraph("📈 Market Trends", styles['Heading2']))
        trend_data = []
        for i, trend in enumerate(analysis_data["trends"], 1):
            trend_data.append([f"{i}.", trend])
        
        if trend_data:
            trend_table = Table(trend_data, colWidths=[0.5*inch, 4*inch])
            trend_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(trend_table)
        story.append(Spacer(1, 20))
    
    # Recommendations Section
    if analysis_data.get("recommendations"):
        story.append(Paragraph("💡 Recommendations", styles['Heading2']))
        story.append(Paragraph(analysis_data["recommendations"], styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Summary
    story.append(Paragraph("📊 Analysis Summary", styles['Heading2']))
    summary_text = f"""
    This analysis was conducted for the product line: {product_line}.
    
    Key Findings:
    • Found {len(analysis_data.get('competitors', []))} major competitors
    • Identified {len(analysis_data.get('trends', []))} market trends
    • Generated comprehensive recommendations for market entry and strategy
    
    This report was generated using MarketMate AI's advanced market analysis capabilities.
    """
    story.append(Paragraph(summary_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def run_market_analysis(product_line):
    """Run the MarketMate AI analysis"""
    try:
        # Initialize MCP Server and get memory store
        mcp_server = MCPServer()
        memory_store = mcp_server.get_memory_store()
        graph = MarketGraph(memory_store)
        
        # Initial state
        initial_state = {
            "product_line": product_line,
            "competitors": [],
            "reviews": {},
            "trends": [],
            "recommendations": None,
            "report_file": None,
            "historical_data": None,
            "preferred_region": st.session_state.get("preferred_region", "Madhya Pradesh, India")
        }
        
        # Run analysis
        with st.spinner("Running MarketMate AI Analysis..."):
            final_state = graph.run_graph(initial_state)
        
        return final_state, None
    except Exception as e:
        st.error(f"Analysis failed: {e}")
        return None, str(e)

def display_predictive_analytics(forecast_data):
    """Display predictive analytics results"""
    if not forecast_data:
        return
    
    st.markdown("### 🔮 Predictive Analytics")
    
    # Sales Forecast
    if forecast_data.get("sales_forecast"):
        with st.expander("📈 Sales Forecast (Next 12 Months)", expanded=True):
            sales_data = forecast_data["sales_forecast"]
            months = [item['month'] for item in sales_data]
            sales = [item['predicted_sales'] for item in sales_data]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months,
                y=sales,
                mode='lines+markers',
                name='Predicted Sales',
                line=dict(color='#1f77b4', width=3)
            ))
            fig.update_layout(
                title="Sales Forecast",
                xaxis_title="Month",
                yaxis_title="Predicted Sales",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Market Growth
    if forecast_data.get("market_growth"):
        with st.expander("📊 Market Growth Projection", expanded=True):
            growth_data = forecast_data["market_growth"]
            periods = [item['period'] for item in growth_data]
            growth_rates = [item['predicted_growth'] for item in growth_data]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=periods,
                y=growth_rates,
                name='Growth Rate',
                marker_color='#2ca02c'
            ))
            fig.update_layout(
                title="Market Growth Projection",
                xaxis_title="Period",
                yaxis_title="Growth Rate",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Competitor Strategies
    if forecast_data.get("competitor_strategies"):
        with st.expander("🎯 Competitor Strategy Predictions", expanded=True):
            for strategy in forecast_data["competitor_strategies"]:
                st.markdown(f"**{strategy['competitor']}** (Risk: {strategy['risk_level']})")
                for pred in strategy['predicted_strategies']:
                    st.markdown(f"• {pred['strategy']} ({pred['probability']:.1%} probability, {pred['timeline']})")
                st.markdown(f"*Recommended Response: {strategy['recommended_response']}*")
                st.markdown("---")
    
    # Price Trends
    if forecast_data.get("price_trends"):
        with st.expander("💰 Price Trend Forecasting", expanded=True):
            price_data = forecast_data["price_trends"]
            months = [item['month'] for item in price_data]
            prices = [item['predicted_price'] for item in price_data]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=months,
                y=prices,
                mode='lines+markers',
                name='Predicted Price',
                line=dict(color='#d62728', width=3)
            ))
            fig.update_layout(
                title="Price Trend Forecasting",
                xaxis_title="Month",
                yaxis_title="Predicted Price ($)",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Seasonal Demand Analysis
    if forecast_data.get("seasonal_analysis"):
        with st.expander("🌸 Seasonal Demand Analysis", expanded=True):
            seasonal_data = forecast_data["seasonal_analysis"]
            seasons = [item['season'] for item in seasonal_data]
            demand_levels = [item['demand_level'] for item in seasonal_data]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=seasons,
                y=demand_levels,
                name='Demand Level',
                marker_color='#9467bd'
            ))
            fig.update_layout(
                title="Seasonal Demand Patterns",
                xaxis_title="Season",
                yaxis_title="Demand Level",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Display seasonal recommendations
            st.markdown("**Seasonal Recommendations:**")
            for item in seasonal_data:
                st.markdown(f"• **{item['season']}**: {item['recommendation']} (Trend: {item['trend']})")

def display_advanced_visualizations(analysis_data, product_line="Product"):
    """Display advanced visualizations"""
    try:
        from utils.advanced_visualizer import get_visualizer
        
        visualizer = get_visualizer()
        if visualizer:
            st.markdown("### 📊 Advanced Visualizations")
            
            # Market Share Pie Chart
            if analysis_data.get("competitors"):
                with st.expander("🥧 Market Share Distribution", expanded=True):
                    fig = visualizer.create_market_share_pie(analysis_data["competitors"])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            # Sentiment Trend
            with st.expander("📈 Sentiment Trends", expanded=True):
                fig = visualizer.create_sentiment_trend_line(None, product_line)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Competitor Radar
            if analysis_data.get("competitors"):
                with st.expander("🎯 Competitor Performance Comparison", expanded=True):
                    fig = visualizer.create_competitor_radar(analysis_data["competitors"])
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
            
            # Price Analysis
            with st.expander("💰 Price Distribution Analysis", expanded=True):
                fig = visualizer.create_price_histogram(None, product_line)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Geographic Heatmap
            with st.expander("🗺️ Geographic Market Distribution", expanded=True):
                fig = visualizer.create_geographic_heatmap(None, product_line)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Market Growth Chart
            with st.expander("📊 Market Growth Trends", expanded=True):
                fig = visualizer.create_market_growth_chart(None, product_line)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
            
            # Seasonal Analysis
            with st.expander("🌸 Seasonal Demand Analysis", expanded=True):
                fig = visualizer.create_seasonal_analysis(None, product_line)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                    
    except Exception as e:
        st.error(f"Error loading visualizations: {e}")
        st.info("Advanced visualizations will be displayed here once the visualizer is implemented.")

# Main Streamlit app
def main():
    st.markdown('<h1 class="main-header">🎤 MarketMate AI - Advanced Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Initialize voice components
    recognizer, engine = init_voice()
    
    # Sidebar for controls
    with st.sidebar:
        st.markdown('<h3 class="sub-header">🎤 Voice Controls</h3>', unsafe_allow_html=True)
        
        # Voice input button
        if st.button("🎤 Start Voice Input", key="voice_input"):
            if recognizer:
                text = listen_for_speech(recognizer)
                if text:
                    st.session_state.product_line = text
                    st.success(f"Product line set to: {text}")
            else:
                st.error("Voice recognition not available")
        
        # Voice output toggle
        voice_output = st.checkbox("🔊 Enable Voice Output", value=True)
        
        st.markdown("---")
        st.markdown("### 📊 Analysis Options")
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Full Market Analysis", "Competitor Analysis", "Trend Analysis", "Review Analysis"]
        )

        # Preferred competitor region (priority: MP → India → Global)
        preferred_region = st.selectbox(
            "Preferred Competitor Region",
            ["Madhya Pradesh, India", "India (All States)", "Global"],
            help="Competitors will be selected with this priority."
        )
        st.session_state["preferred_region"] = preferred_region
        
        st.markdown("---")
        st.markdown("### 🎨 Visualization Options")
        
        # MCP Server Status
        try:
            mcp_server = MCPServer()
            server_status = mcp_server.get_server_status()
            with st.expander("🔧 MCP Server Status", expanded=False):
                st.json(server_status)
        except Exception as e:
            st.error(f"MCP Server status unavailable: {e}")
        
        # Quick visualization button
        if st.button("📊 Quick Visualize", help="Generate visualizations for current product line"):
            if "product_line" in st.session_state and st.session_state.product_line:
                st.session_state.show_visualizations = True
                st.success("Visualizations will be displayed below!")
            else:
                st.warning("Please enter a product line first!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<h2 class="sub-header">📈 Advanced Market Analysis</h2>', unsafe_allow_html=True)
        
        # Product line input
        product_line = st.text_input(
            "Enter Product Line to Analyze:",
            value=st.session_state.get("product_line", ""),
            placeholder="e.g., smartphone accessories, motorcycle brake pads"
        )
        
        # Display Quick Visualizations if requested
        if st.session_state.get("show_visualizations", False) and "product_line" in st.session_state:
            st.markdown("### 🎨 Quick Visualizations")
            st.info(f"Generating visualizations for: **{st.session_state.product_line}**")
            
            # Use actual analysis data if available, otherwise run quick analysis
            if "analysis_complete" in st.session_state and st.session_state.analysis_complete:
                # Use existing analysis data
                analysis_data = st.session_state.analysis_data
                st.success("Using previous analysis results for visualizations")
            else:
                # Run quick analysis for visualizations only
                st.info("Running quick analysis for visualizations...")
                with st.spinner("Analyzing market data..."):
                    try:
                        # Initialize MCP Server and get memory store
                        mcp_server = MCPServer()
                        memory_store = mcp_server.get_memory_store()
                        graph = MarketGraph(memory_store)
                        
                        # Quick analysis state
                        initial_state = {
                            "product_line": st.session_state.product_line,
                            "competitors": [],
                            "reviews": {},
                            "trends": [],
                            "recommendations": None,
                            "report_file": None,
                            "historical_data": None,
                            "preferred_region": st.session_state.get("preferred_region", "Madhya Pradesh, India")
                        }
                        
                        # Run analysis with progress tracking
                        print("Starting full market analysis...")
                        final_state = graph.run_graph(initial_state)
                        print("Analysis completed successfully!")
                        analysis_data = {
                            "competitors": final_state.get("competitors", []),
                            "trends": final_state.get("trends", []),
                            "recommendations": final_state.get("recommendations", "No recommendations available")
                        }
                        st.success("Quick analysis completed!")
                    except Exception as e:
                        st.error(f"Error in quick analysis: {e}")
                        # Fallback to sample data
                        analysis_data = {
                            "competitors": ["Sample Competitor 1", "Sample Competitor 2", "Sample Competitor 3"],
                            "trends": ["Sample Trend 1", "Sample Trend 2"],
                            "recommendations": "Sample recommendations"
                        }
            
            # Display Advanced Visualizations
            display_advanced_visualizations(analysis_data, st.session_state.product_line)
            
            # Add comprehensive dashboard
            try:
                from utils.advanced_visualizer import get_visualizer
                visualizer = get_visualizer()
                if visualizer:
                    with st.expander("📊 Comprehensive Dashboard View", expanded=True):
                        fig = visualizer.create_comprehensive_dashboard(analysis_data, st.session_state.product_line)
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating comprehensive dashboard: {e}")
            
            st.markdown("---")
        
        # Display previous analysis results if available
        if "analysis_complete" in st.session_state and st.session_state.analysis_complete:
            st.markdown("### 📊 Previous Analysis Results")
            
            analysis_data = st.session_state.analysis_data
            if analysis_data.get("competitors"):
                st.markdown("#### 🏢 Competitors Found")
                for competitor in analysis_data["competitors"]:
                    st.write(f"- {competitor}")
            
            if analysis_data.get("trends"):
                st.markdown("#### 📈 Market Trends")
                for trend in analysis_data["trends"]:
                    st.write(f"- {trend}")
            
            if analysis_data.get("recommendations"):
                st.markdown("#### 💡 Recommendations")
                st.write(analysis_data["recommendations"])
            
            # Display Advanced Visualizations
            display_advanced_visualizations(analysis_data, st.session_state.get("product_line", "Product"))
            
            # Display Predictive Analytics
            if analysis_data.get("predictive_analytics"):
                display_predictive_analytics(analysis_data["predictive_analytics"])
            
            # PDF Download for previous analysis
            st.markdown("---")
            st.markdown("### 📄 Download Previous Report")
            
            pdf_buffer = create_pdf_report(analysis_data, st.session_state.product_line)
            filename = f"market_analysis_{st.session_state.product_line.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            
            st.download_button(
                label="📥 Download Previous PDF Report",
                data=pdf_buffer.getvalue(),
                file_name=filename,
                mime="application/pdf",
                help="Click to download the previous analysis report in PDF format",
                key="previous_pdf_download_button"
            )
            
            st.markdown("---")
        
        col1_button, col2_button = st.columns([1, 1])
        
        with col1_button:
            if st.button("🚀 Run Advanced Analysis", type="primary"):
                if product_line:
                    st.session_state.product_line = product_line
                    
                    # Run the analysis
                    # Include preferred region in the analysis state
                    final_state, error = run_market_analysis(product_line)
                    if final_state is not None and "preferred_region" not in final_state:
                        final_state["preferred_region"] = st.session_state.get("preferred_region", "Madhya Pradesh, India")
                
                if final_state:
                    st.success("✅ Advanced analysis completed successfully!")
                    
                    # Store analysis data in session state
                    st.session_state.analysis_complete = True
                    st.session_state.analysis_data = final_state
                    st.session_state.product_line = product_line
                    
                    # Display results
                    if final_state.get("competitors"):
                        st.markdown("### 🏢 Competitors Found")
                        for competitor in final_state["competitors"]:
                            st.write(f"- {competitor}")
                    
                    if final_state.get("trends"):
                        st.markdown("### 📈 Market Trends")
                        for trend in final_state["trends"]:
                            st.write(f"- {trend}")
                    
                    if final_state.get("recommendations"):
                        st.markdown("### 💡 Advanced Recommendations")
                        st.write(final_state["recommendations"])
                    
                    # Display Advanced Visualizations
                    display_advanced_visualizations(final_state, product_line)
                    
                    # Display Predictive Analytics
                    if final_state.get("predictive_analytics"):
                        display_predictive_analytics(final_state["predictive_analytics"])
                    
                    # PDF Download Section
                    st.markdown("---")
                    st.markdown("### 📄 Download Advanced Report")
                    
                    # Create PDF
                    pdf_buffer = create_pdf_report(final_state, product_line)
                    
                    # Generate download link
                    filename = f"advanced_market_analysis_{product_line.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    
                    # Use Streamlit's native download button for better visibility
                    st.download_button(
                        label="📥 Download Advanced PDF Report",
                        data=pdf_buffer.getvalue(),
                        file_name=filename,
                        mime="application/pdf",
                        help="Click to download your comprehensive advanced market analysis report in PDF format",
                        key="pdf_download_button"
                    )
                    
                    st.success("✅ Advanced PDF report is ready! Click the button above to download.")
                    
                    # Voice output
                    if voice_output and engine:
                        summary = f"Advanced analysis complete for {product_line}. Found {len(final_state.get('competitors', []))} competitors. Predictive analytics and visualizations generated. Advanced PDF report is ready for download."
                        speak_text(engine, summary)
                else:
                    st.error(f"❌ Analysis failed: {error}")
            else:
                st.warning("⚠️ Please enter a product line to analyze")
        
        with col2_button:
            if st.button("🗑️ Clear Analysis", type="secondary"):
                # Clear session state
                if "analysis_complete" in st.session_state:
                    del st.session_state.analysis_complete
                if "analysis_data" in st.session_state:
                    del st.session_state.analysis_data
                if "product_line" in st.session_state:
                    del st.session_state.product_line
                if "show_visualizations" in st.session_state:
                    del st.session_state.show_visualizations
                st.success("✅ Analysis data cleared!")
                st.rerun()
        
        # Additional visualization controls
        if st.session_state.get("show_visualizations", False):
            if st.button("❌ Hide Visualizations", type="secondary"):
                st.session_state.show_visualizations = False
                st.rerun()
    
    with col2:
        st.markdown('<h3 class="sub-header">📊 Advanced Metrics</h3>', unsafe_allow_html=True)
        
        # Display session stats
        if "product_line" in st.session_state:
            st.metric("Current Product", st.session_state.product_line)
        
        # Voice status
        voice_status = "✅ Available" if recognizer and engine else "❌ Not Available"
        st.metric("Voice System", voice_status)
        
        # Analysis status
        if "analysis_complete" in st.session_state:
            st.metric("Last Analysis", "✅ Complete")
            
            # Advanced metrics
            analysis_data = st.session_state.analysis_data
            if analysis_data.get("predictive_analytics"):
                pred_data = analysis_data["predictive_analytics"]
                if pred_data.get("sales_forecast"):
                    avg_sales = sum([f['predicted_sales'] for f in pred_data["sales_forecast"]]) / len(pred_data["sales_forecast"])
                    st.metric("Avg Predicted Sales", f"{avg_sales:,.0f}")
                
                if pred_data.get("market_growth"):
                    avg_growth = sum([g['predicted_growth'] for g in pred_data["market_growth"]]) / len(pred_data["market_growth"])
                    st.metric("Avg Growth Rate", f"{avg_growth:.1%}")
        else:
            st.metric("Last Analysis", "⏳ Pending")
        
        # PDF Download Status
        if "analysis_complete" in st.session_state:
            st.metric("Advanced Report", "📄 Ready")
        else:
            st.metric("Advanced Report", "⏳ Pending")

if __name__ == "__main__":
    main()
  