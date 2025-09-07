import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import numpy as np
import folium
from geopy.geocoders import Nominatim
from datetime import datetime, timedelta
import random
import json

class AdvancedVisualizer:
    """Advanced visualization class for market analysis data"""
    
    def __init__(self):
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def create_market_share_pie(self, competitors, market_shares=None):
        """Create market share pie chart"""
        try:
            if not market_shares:
                # Generate realistic market shares if not provided
                total = 100
                shares = []
                for i in range(len(competitors)):
                    if i == len(competitors) - 1:
                        shares.append(total)
                    else:
                        share = random.randint(5, 30)
                        shares.append(share)
                        total -= share
                market_shares = shares
            
            fig = go.Figure(data=[go.Pie(
                labels=competitors,
                values=market_shares,
                hole=0.3,
                marker_colors=self.colors[:len(competitors)]
            )])
            
            fig.update_layout(
                title="Market Share Distribution",
                title_x=0.5,
                showlegend=True,
                height=500
            )
            
            return fig
        except Exception as e:
            print(f"Error creating market share pie chart: {e}")
            return None
    
    def create_sentiment_trend_line(self, sentiment_data):
        """Create sentiment trend line chart"""
        try:
            # Generate sample sentiment data if not provided
            if not sentiment_data:
                dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
                sentiment_scores = [random.uniform(0.3, 0.9) for _ in range(len(dates))]
                sentiment_data = pd.DataFrame({
                    'date': dates,
                    'sentiment_score': sentiment_scores
                })
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sentiment_data['date'],
                y=sentiment_data['sentiment_score'],
                mode='lines+markers',
                name='Sentiment Score',
                line=dict(color='#2ca02c', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="Customer Sentiment Trends Over Time",
                title_x=0.5,
                xaxis_title="Date",
                yaxis_title="Sentiment Score",
                height=400,
                showlegend=True
            )
            
            return fig
        except Exception as e:
            print(f"Error creating sentiment trend line: {e}")
            return None
    
    def create_competitor_radar(self, competitors, metrics_data=None):
        """Create competitor comparison radar chart"""
        try:
            if not metrics_data:
                # Generate sample metrics data
                metrics = ['Market Share', 'Customer Satisfaction', 'Price Competitiveness', 
                          'Brand Recognition', 'Innovation Score', 'Distribution Reach']
                metrics_data = {}
                
                for competitor in competitors:
                    metrics_data[competitor] = [random.randint(60, 95) for _ in range(len(metrics))]
            
            fig = go.Figure()
            
            for i, competitor in enumerate(competitors):
                fig.add_trace(go.Scatterpolar(
                    r=metrics_data[competitor],
                    theta=metrics,
                    fill='toself',
                    name=competitor,
                    line_color=self.colors[i % len(self.colors)]
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Competitor Performance Comparison",
                title_x=0.5,
                height=500
            )
            
            return fig
        except Exception as e:
            print(f"Error creating competitor radar chart: {e}")
            return None
    
    def create_price_histogram(self, price_data=None):
        """Create price analysis histogram"""
        try:
            if not price_data:
                # Generate sample price data
                price_data = np.random.normal(150, 50, 1000)  # Normal distribution around $150
            
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=price_data,
                nbinsx=30,
                marker_color='#1f77b4',
                opacity=0.7
            ))
            
            fig.update_layout(
                title="Price Distribution Analysis",
                title_x=0.5,
                xaxis_title="Price ($)",
                yaxis_title="Frequency",
                height=400,
                showlegend=False
            )
            
            return fig
        except Exception as e:
            print(f"Error creating price histogram: {e}")
            return None
    
    def create_geographic_heatmap(self, location_data=None):
        """Create geographic market heatmap"""
        try:
            if not location_data:
                # Generate sample location data
                cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                         'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
                market_sizes = [random.randint(1000, 10000) for _ in range(len(cities))]
                location_data = list(zip(cities, market_sizes))
            
            # Create a map centered on US
            m = folium.Map(location=[39.8283, -98.5795], zoom_start=4)
            
            # Add markers for each location
            for city, market_size in location_data:
                try:
                    geolocator = Nominatim(user_agent="marketmate_ai")
                    location = geolocator.geocode(city + ", USA")
                    
                    if location:
                        # Color based on market size
                        if market_size > 7000:
                            color = 'red'
                        elif market_size > 5000:
                            color = 'orange'
                        elif market_size > 3000:
                            color = 'yellow'
                        else:
                            color = 'green'
                        
                        folium.CircleMarker(
                            location=[location.latitude, location.longitude],
                            radius=market_size/500,
                            popup=f"{city}: {market_size:,} market size",
                            color=color,
                            fill=True
                        ).add_to(m)
                except Exception as e:
                    print(f"Error geocoding {city}: {e}")
                    continue
            
            return m
        except Exception as e:
            print(f"Error creating geographic heatmap: {e}")
            return None
    
    def create_comprehensive_dashboard(self, analysis_data):
        """Create a comprehensive dashboard with all visualizations"""
        try:
            # Create subplots
            fig = sp.make_subplots(
                rows=3, cols=2,
                subplot_titles=('Market Share', 'Sentiment Trends', 'Competitor Radar', 
                              'Price Distribution', 'Market Growth', 'Seasonal Analysis'),
                specs=[[{"type": "pie"}, {"type": "scatter"}],
                       [{"type": "scatterpolar"}, {"type": "histogram"}],
                       [{"type": "bar"}, {"type": "scatter"}]]
            )
            
            # Market Share Pie Chart
            if analysis_data.get('competitors'):
                competitors = analysis_data['competitors']
                market_shares = [random.randint(10, 40) for _ in range(len(competitors))]
                fig.add_trace(
                    go.Pie(labels=competitors, values=market_shares, name="Market Share"),
                    row=1, col=1
                )
            
            # Sentiment Trend Line
            dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
            sentiment_scores = [random.uniform(0.3, 0.9) for _ in range(len(dates))]
            fig.add_trace(
                go.Scatter(x=dates, y=sentiment_scores, name="Sentiment"),
                row=1, col=2
            )
            
            # Competitor Radar (simplified as scatter)
            if analysis_data.get('competitors'):
                metrics = ['Share', 'Satisfaction', 'Price', 'Brand', 'Innovation']
                for i, competitor in enumerate(competitors[:3]):  # Top 3 competitors
                    scores = [random.randint(60, 95) for _ in range(len(metrics))]
                    fig.add_trace(
                        go.Scatter(x=metrics, y=scores, name=competitor, mode='lines+markers'),
                        row=2, col=1
                    )
            
            # Price Histogram
            price_data = np.random.normal(150, 50, 1000)
            fig.add_trace(
                go.Histogram(x=price_data, name="Price Distribution"),
                row=2, col=2
            )
            
            # Market Growth Bar Chart
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            growth_rates = [random.uniform(5, 25) for _ in range(len(months))]
            fig.add_trace(
                go.Bar(x=months, y=growth_rates, name="Growth Rate"),
                row=3, col=1
            )
            
            # Seasonal Analysis
            seasons = ['Q1', 'Q2', 'Q3', 'Q4']
            seasonal_demand = [random.randint(80, 120) for _ in range(len(seasons))]
            fig.add_trace(
                go.Scatter(x=seasons, y=seasonal_demand, name="Seasonal Demand", mode='lines+markers'),
                row=3, col=2
            )
            
            fig.update_layout(height=1200, showlegend=True, title_text="MarketMate AI - Comprehensive Market Analysis Dashboard")
            
            return fig
        except Exception as e:
            print(f"Error creating comprehensive dashboard: {e}")
            return None

