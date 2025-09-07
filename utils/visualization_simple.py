import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
from datetime import datetime, timedelta
import random
import json

class SimpleVisualizer:
    """Simplified visualization class for market analysis data"""
    
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
    
    def create_sentiment_trend_line(self, sentiment_data=None):
        """Create sentiment trend line chart"""
        try:
            # Generate sample sentiment data if not provided
            if not sentiment_data:
                dates = [datetime.now() - timedelta(days=i*30) for i in range(12, 0, -1)]
                sentiment_scores = [random.uniform(0.3, 0.9) for _ in range(len(dates))]
            else:
                dates = sentiment_data.get('dates', [])
                sentiment_scores = sentiment_data.get('scores', [])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=sentiment_scores,
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
        """Create geographic market heatmap using Plotly"""
        try:
            if not location_data:
                # Generate sample location data
                cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                         'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
                market_sizes = [random.randint(1000, 10000) for _ in range(len(cities))]
                location_data = list(zip(cities, market_sizes))
            
            # Create a simple scatter plot on a map using Plotly
            cities = [item[0] for item in location_data]
            market_sizes = [item[1] for item in location_data]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scattergeo(
                lon=[-74.006, -118.243, -87.629, -95.369, -112.074, -75.165, -98.494, -117.161, -96.797, -121.886],
                lat=[40.712, 34.052, 41.878, 29.760, 33.448, 39.952, 29.424, 32.715, 32.776, 37.338],
                mode='markers',
                marker=dict(
                    size=[size/500 for size in market_sizes],
                    color=market_sizes,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Market Size")
                ),
                text=cities,
                hovertemplate="<b>%{text}</b><br>Market Size: %{marker.color:,}<extra></extra>"
            ))
            
            fig.update_layout(
                title="Geographic Market Distribution",
                title_x=0.5,
                geo=dict(
                    scope='usa',
                    projection_type='albers usa',
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    coastlinecolor='rgb(204, 204, 204)',
                ),
                height=500
            )
            
            return fig
        except Exception as e:
            print(f"Error creating geographic heatmap: {e}")
            return None
