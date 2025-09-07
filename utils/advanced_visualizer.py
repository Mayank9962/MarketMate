import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
import numpy as np
from datetime import datetime, timedelta
import random
import json
import os

class AdvancedVisualizer:
    """Advanced visualization class for MarketMate AI dashboard"""
    
    def __init__(self):
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    def create_market_share_pie(self, competitors, market_shares=None):
        """Create market share pie chart"""
        try:
            if not competitors:
                return None
                
            if not market_shares:
                # Generate realistic market shares if not provided
                total = 100
                shares = []
                for i in range(len(competitors)):
                    if i == len(competitors) - 1:
                        shares.append(max(1, total))  # Ensure last gets remaining
                    else:
                        share = random.randint(5, min(35, total - (len(competitors) - i - 1)))
                        shares.append(share)
                        total -= share
                market_shares = shares
            
            fig = go.Figure(data=[go.Pie(
                labels=competitors,
                values=market_shares,
                hole=0.3,
                marker_colors=self.colors[:len(competitors)],
                textinfo='label+percent',
                textposition='outside'
            )])
            
            fig.update_layout(
                title="🥧 Market Share Distribution",
                title_x=0.5,
                showlegend=True,
                height=500,
                font=dict(size=12)
            )
            
            return fig
        except Exception as e:
            print(f"Error creating market share pie chart: {e}")
            return None
    
    def create_sentiment_trend_line(self, sentiment_data=None, product_line="Product"):
        """Create sentiment trend line chart"""
        try:
            # Generate sample sentiment data if not provided
            if not sentiment_data:
                # Use pure-Python dates to avoid pandas initialization issues
                dates = [datetime(2024, i, 1) for i in range(1, 13)]
                # Create more realistic sentiment trends
                base_sentiment = 0.6
                trend = np.linspace(0, 0.3, len(dates))
                noise = np.random.normal(0, 0.1, len(dates))
                sentiment_scores = np.clip(base_sentiment + trend + noise, 0.1, 0.95)
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
                marker=dict(size=8, color='#2ca02c'),
                fill='tonexty',
                fillcolor='rgba(44, 160, 44, 0.1)'
            ))
            
            # Add trend line
            z = np.polyfit(range(len(dates)), sentiment_scores, 1)
            p = np.poly1d(z)
            trend_line = p(range(len(dates)))
            
            fig.add_trace(go.Scatter(
                x=dates,
                y=trend_line,
                mode='lines',
                name='Trend',
                line=dict(color='#d62728', width=2, dash='dash')
            ))
            
            fig.update_layout(
                title=f"📈 {product_line} - Customer Sentiment Trends",
                title_x=0.5,
                xaxis_title="Date",
                yaxis_title="Sentiment Score (0-1)",
                height=400,
                showlegend=True,
                hovermode='x unified'
            )
            
            return fig
        except Exception as e:
            print(f"Error creating sentiment trend line: {e}")
            return None
    
    def create_competitor_radar(self, competitors, metrics_data=None):
        """Create competitor comparison radar chart"""
        try:
            if not competitors:
                return None
                
            if not metrics_data:
                # Generate sample metrics data
                metrics = ['Market Share', 'Customer Satisfaction', 'Price Competitiveness', 
                          'Brand Recognition', 'Innovation Score', 'Distribution Reach']
                metrics_data = {}
                
                for i, competitor in enumerate(competitors):
                    # Create realistic variations in metrics
                    base_scores = [75, 80, 70, 85, 60, 75]
                    variation = np.random.normal(0, 10, len(metrics))
                    scores = np.clip([base + var for base, var in zip(base_scores, variation)], 20, 100)
                    metrics_data[competitor] = scores.tolist()
            
            fig = go.Figure()
            
            for i, competitor in enumerate(competitors[:5]):  # Limit to top 5 competitors
                fig.add_trace(go.Scatterpolar(
                    r=metrics_data[competitor],
                    theta=metrics,
                    fill='toself',
                    name=competitor,
                    line_color=self.colors[i % len(self.colors)],
                    opacity=0.6
                ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont=dict(size=10)
                    )),
                showlegend=True,
                title="🎯 Competitor Performance Comparison",
                title_x=0.5,
                height=500,
                font=dict(size=11)
            )
            
            return fig
        except Exception as e:
            print(f"Error creating competitor radar chart: {e}")
            return None
    
    def create_price_histogram(self, price_data=None, product_line="Product"):
        """Create price analysis histogram"""
        try:
            if not price_data:
                # Generate sample price data based on product line
                if "smartphone" in product_line.lower():
                    price_data = np.random.normal(25, 15, 1000)  # $10-40 range
                elif "motorcycle" in product_line.lower() or "bike" in product_line.lower():
                    price_data = np.random.normal(80, 30, 1000)  # $20-140 range
                elif "electronics" in product_line.lower():
                    price_data = np.random.normal(150, 50, 1000)  # $50-250 range
                else:
                    price_data = np.random.normal(100, 40, 1000)  # $20-180 range
            
            fig = go.Figure()
            
            fig.add_trace(go.Histogram(
                x=price_data,
                nbinsx=30,
                marker_color='#1f77b4',
                opacity=0.7,
                name='Price Distribution'
            ))
            
            # Add mean line
            mean_price = np.mean(price_data)
            fig.add_vline(x=mean_price, line_dash="dash", line_color="red", 
                         annotation_text=f"Mean: ${mean_price:.2f}")
            
            fig.update_layout(
                title=f"💰 {product_line} - Price Distribution Analysis",
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
    
    def create_geographic_heatmap(self, location_data=None, product_line="Product"):
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
            
            # US city coordinates
            city_coords = {
                'New York': (-74.006, 40.712),
                'Los Angeles': (-118.243, 34.052),
                'Chicago': (-87.629, 41.878),
                'Houston': (-95.369, 29.760),
                'Phoenix': (-112.074, 33.448),
                'Philadelphia': (-75.165, 39.952),
                'San Antonio': (-98.494, 29.424),
                'San Diego': (-117.161, 32.715),
                'Dallas': (-96.797, 32.776),
                'San Jose': (-121.886, 37.338)
            }
            
            lons = [city_coords[city][0] for city in cities if city in city_coords]
            lats = [city_coords[city][1] for city in cities if city in city_coords]
            sizes = [market_sizes[i] for i, city in enumerate(cities) if city in city_coords]
            city_names = [city for city in cities if city in city_coords]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scattergeo(
                lon=lons,
                lat=lats,
                mode='markers',
                marker=dict(
                    size=[max(5, size/200) for size in sizes],
                    color=sizes,
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Market Size"),
                    line=dict(width=1, color='white')
                ),
                text=city_names,
                hovertemplate="<b>%{text}</b><br>Market Size: %{marker.color:,}<extra></extra>"
            ))
            
            fig.update_layout(
                title=f"🗺️ {product_line} - Geographic Market Distribution",
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
    
    def create_market_growth_chart(self, growth_data=None, product_line="Product"):
        """Create market growth bar chart"""
        try:
            if not growth_data:
                # Generate sample growth data
                months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                growth_rates = [random.uniform(5, 25) for _ in range(len(months))]
            else:
                months = growth_data.get('months', [])
                growth_rates = growth_data.get('rates', [])
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=months,
                y=growth_rates,
                name='Growth Rate (%)',
                marker_color='#2ca02c',
                text=[f"{rate:.1f}%" for rate in growth_rates],
                textposition='outside'
            ))
            
            fig.update_layout(
                title=f"📊 {product_line} - Market Growth Trends",
                title_x=0.5,
                xaxis_title="Month",
                yaxis_title="Growth Rate (%)",
                height=400,
                showlegend=False
            )
            
            return fig
        except Exception as e:
            print(f"Error creating market growth chart: {e}")
            return None
    
    def create_seasonal_analysis(self, seasonal_data=None, product_line="Product"):
        """Create seasonal demand analysis"""
        try:
            if not seasonal_data:
                # Generate sample seasonal data
                seasons = ['Q1 (Winter)', 'Q2 (Spring)', 'Q3 (Summer)', 'Q4 (Fall)']
                demand_levels = [random.randint(80, 120) for _ in range(len(seasons))]
                trends = ['Rising', 'Stable', 'Falling', 'Rising']
            else:
                seasons = seasonal_data.get('seasons', [])
                demand_levels = seasonal_data.get('demand', [])
                trends = seasonal_data.get('trends', [])
            
            fig = go.Figure()
            
            fig.add_trace(go.Bar(
                x=seasons,
                y=demand_levels,
                name='Demand Level',
                marker_color='#9467bd',
                text=[f"{level}%" for level in demand_levels],
                textposition='outside'
            ))
            
            fig.update_layout(
                title=f"🌸 {product_line} - Seasonal Demand Analysis",
                title_x=0.5,
                xaxis_title="Season",
                yaxis_title="Demand Level (%)",
                height=400,
                showlegend=False
            )
            
            return fig
        except Exception as e:
            print(f"Error creating seasonal analysis: {e}")
            return None
    
    def create_comprehensive_dashboard(self, analysis_data, product_line="Product"):
        """Create a comprehensive dashboard with all visualizations"""
        try:
            # Create subplots
            fig = sp.make_subplots(
                rows=3, cols=2,
                subplot_titles=('Market Share Distribution', 'Sentiment Trends', 
                              'Competitor Performance', 'Price Distribution', 
                              'Market Growth', 'Seasonal Analysis'),
                specs=[[{"type": "pie"}, {"type": "scatter"}],
                       [{"type": "scatter"}, {"type": "histogram"}],
                       [{"type": "bar"}, {"type": "bar"}]],
                vertical_spacing=0.08,
                horizontal_spacing=0.08
            )
            
            # Market Share Pie Chart
            if analysis_data.get('competitors'):
                competitors = analysis_data['competitors']
                market_shares = [random.randint(10, 40) for _ in range(len(competitors))]
                fig.add_trace(
                    go.Pie(labels=competitors, values=market_shares, name="Market Share", 
                          marker_colors=self.colors[:len(competitors)]),
                    row=1, col=1
                )
            
            # Sentiment Trend Line
            dates = [datetime(2024, i, 1) for i in range(1, 13)]
            sentiment_scores = [random.uniform(0.3, 0.9) for _ in range(len(dates))]
            fig.add_trace(
                go.Scatter(x=dates, y=sentiment_scores, name="Sentiment", 
                          line=dict(color='#2ca02c', width=3)),
                row=1, col=2
            )
            
            # Competitor Radar (simplified as scatter)
            if analysis_data.get('competitors'):
                metrics = ['Share', 'Satisfaction', 'Price', 'Brand', 'Innovation']
                for i, competitor in enumerate(analysis_data['competitors'][:3]):
                    scores = [random.randint(60, 95) for _ in range(len(metrics))]
                    fig.add_trace(
                        go.Scatter(x=metrics, y=scores, name=competitor, 
                                 mode='lines+markers', line_color=self.colors[i]),
                        row=2, col=1
                    )
            
            # Price Histogram
            price_data = np.random.normal(100, 40, 1000)
            fig.add_trace(
                go.Histogram(x=price_data, name="Price Distribution", 
                           marker_color='#1f77b4', opacity=0.7),
                row=2, col=2
            )
            
            # Market Growth Bar Chart
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            growth_rates = [random.uniform(5, 25) for _ in range(len(months))]
            fig.add_trace(
                go.Bar(x=months, y=growth_rates, name="Growth Rate", 
                      marker_color='#2ca02c'),
                row=3, col=1
            )
            
            # Seasonal Analysis
            seasons = ['Q1', 'Q2', 'Q3', 'Q4']
            seasonal_demand = [random.randint(80, 120) for _ in range(len(seasons))]
            fig.add_trace(
                go.Bar(x=seasons, y=seasonal_demand, name="Seasonal Demand", 
                      marker_color='#9467bd'),
                row=3, col=2
            )
            
            fig.update_layout(
                height=1200, 
                showlegend=True, 
                title_text=f"📊 {product_line} - Comprehensive Market Analysis Dashboard",
                title_x=0.5,
                font=dict(size=12)
            )
            
            return fig
        except Exception as e:
            print(f"Error creating comprehensive dashboard: {e}")
            return None

def get_visualizer():
    """Get an instance of the advanced visualizer"""
    return AdvancedVisualizer()
