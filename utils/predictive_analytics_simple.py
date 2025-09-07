import numpy as np
import random
from datetime import datetime, timedelta
import json

class SimplePredictiveAnalytics:
    """Simplified predictive analytics class for market analysis"""
    
    def __init__(self):
        self.random_seed = 42
        random.seed(self.random_seed)
        np.random.seed(self.random_seed)
    
    def generate_historical_data(self, product_line, months=24):
        """Generate historical data for analysis"""
        try:
            data = []
            base_date = datetime.now() - timedelta(days=months*30)
            
            for i in range(months):
                date = base_date + timedelta(days=i*30)
                sales = random.randint(1000, 5000)
                price = random.uniform(50, 200)
                sentiment = random.uniform(0.3, 0.9)
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'sales': sales,
                    'price': price,
                    'sentiment': sentiment
                })
            
            return data
        except Exception as e:
            print(f"Error generating historical data: {e}")
            return []
    
    def predict_sales_forecast(self, product_line, months=12):
        """Predict sales forecast for the next months"""
        try:
            # Generate historical data
            historical_data = self.generate_historical_data(product_line)
            
            if not historical_data:
                return []
            
            # Simple linear trend prediction
            sales_trend = [d['sales'] for d in historical_data]
            base_sales = np.mean(sales_trend)
            trend_factor = np.polyfit(range(len(sales_trend)), sales_trend, 1)[0]
            
            # Generate forecast
            forecast = []
            current_date = datetime.now()
            
            for i in range(1, months + 1):
                forecast_date = current_date + timedelta(days=i*30)
                predicted_sales = max(0, int(base_sales + trend_factor * (len(sales_trend) + i) + random.uniform(-200, 200)))
                
                forecast.append({
                    'month': forecast_date.strftime('%Y-%m'),
                    'predicted_sales': predicted_sales,
                    'confidence': random.uniform(0.7, 0.95)
                })
            
            return forecast
        except Exception as e:
            print(f"Error predicting sales forecast: {e}")
            return []
    
    def predict_market_growth(self, product_line, periods=36):
        """Predict market growth over time"""
        try:
            growth_rates = []
            current_date = datetime.now()
            
            # Generate realistic growth rates with seasonal patterns
            for i in range(periods):
                period_date = current_date + timedelta(days=i*30)
                
                # Base growth rate with seasonal variation
                base_growth = 0.05  # 5% base growth
                seasonal_factor = 0.02 * np.sin(2 * np.pi * i / 12)  # Seasonal variation
                random_factor = random.uniform(-0.01, 0.01)
                
                growth_rate = max(-0.1, min(0.2, base_growth + seasonal_factor + random_factor))
                
                growth_rates.append({
                    'period': f"Period {i+1}",
                    'predicted_growth': growth_rate,
                    'date': period_date.strftime('%Y-%m')
                })
            
            return growth_rates
        except Exception as e:
            print(f"Error predicting market growth: {e}")
            return []
    
    def predict_competitor_strategy(self, competitors):
        """Predict competitor strategies"""
        try:
            strategies = []
            strategy_types = [
                'Price Reduction', 'Product Innovation', 'Market Expansion',
                'Partnership Formation', 'Marketing Campaign', 'Supply Chain Optimization'
            ]
            
            for competitor in competitors:
                predicted_strategies = []
                
                # Predict 2-4 strategies per competitor
                num_strategies = random.randint(2, 4)
                selected_strategies = random.sample(strategy_types, num_strategies)
                
                for strategy in selected_strategies:
                    predicted_strategies.append({
                        'strategy': strategy,
                        'probability': random.uniform(0.3, 0.9),
                        'timeline': random.choice(['Immediate', '3 months', '6 months', '12 months']),
                        'impact': random.choice(['Low', 'Medium', 'High'])
                    })
                
                # Determine risk level
                avg_probability = np.mean([s['probability'] for s in predicted_strategies])
                if avg_probability > 0.7:
                    risk_level = 'High'
                elif avg_probability > 0.5:
                    risk_level = 'Medium'
                else:
                    risk_level = 'Low'
                
                # Generate recommended response
                responses = [
                    'Monitor closely and prepare counter-strategy',
                    'Accelerate our own innovation pipeline',
                    'Strengthen customer relationships',
                    'Consider strategic partnerships',
                    'Optimize pricing strategy',
                    'Enhance marketing efforts'
                ]
                
                strategies.append({
                    'competitor': competitor,
                    'predicted_strategies': predicted_strategies,
                    'risk_level': risk_level,
                    'recommended_response': random.choice(responses)
                })
            
            return strategies
        except Exception as e:
            print(f"Error predicting competitor strategy: {e}")
            return []
    
    def predict_price_trends(self, product_line, months=12):
        """Predict price trends over time"""
        try:
            price_trends = []
            current_date = datetime.now()
            base_price = random.uniform(100, 150)
            
            # Generate price trend with inflation and market factors
            for i in range(months):
                forecast_date = current_date + timedelta(days=i*30)
                
                # Price trend factors
                inflation_factor = 0.002 * i  # 0.2% monthly inflation
                market_factor = random.uniform(-0.01, 0.01)  # Market fluctuations
                seasonal_factor = 0.005 * np.sin(2 * np.pi * i / 12)  # Seasonal variation
                
                price_change = inflation_factor + market_factor + seasonal_factor
                predicted_price = max(50, base_price * (1 + price_change))
                
                price_trends.append({
                    'month': forecast_date.strftime('%Y-%m'),
                    'predicted_price': round(predicted_price, 2),
                    'price_change': round(price_change * 100, 2),
                    'confidence': random.uniform(0.6, 0.9)
                })
            
            return price_trends
        except Exception as e:
            print(f"Error predicting price trends: {e}")
            return []
    
    def analyze_seasonal_demand(self, product_line):
        """Analyze seasonal demand patterns"""
        try:
            seasons = ['Q1 (Jan-Mar)', 'Q2 (Apr-Jun)', 'Q3 (Jul-Sep)', 'Q4 (Oct-Dec)']
            seasonal_analysis = []
            
            for i, season in enumerate(seasons):
                # Generate seasonal demand factors
                base_demand = random.uniform(0.8, 1.2)
                seasonal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * i / 4)  # Seasonal pattern
                
                demand_level = base_demand * seasonal_factor
                
                seasonal_analysis.append({
                    'season': season,
                    'demand_level': round(demand_level, 2),
                    'trend': random.choice(['Increasing', 'Stable', 'Decreasing']),
                    'recommendation': self._get_seasonal_recommendation(season, demand_level)
                })
            
            return seasonal_analysis
        except Exception as e:
            print(f"Error analyzing seasonal demand: {e}")
            return []
    
    def _get_seasonal_recommendation(self, season, demand_level):
        """Get recommendation based on seasonal demand"""
        if demand_level > 1.1:
            return "Increase inventory and marketing efforts"
        elif demand_level > 0.9:
            return "Maintain current strategy"
        else:
            return "Consider promotional activities to boost demand"
    
    def generate_comprehensive_forecast(self, product_line, competitors=None):
        """Generate comprehensive forecast with all predictions"""
        try:
            if not competitors:
                competitors = ['Competitor A', 'Competitor B', 'Competitor C']
            
            forecast = {
                'product_line': product_line,
                'generated_at': datetime.now().isoformat(),
                'sales_forecast': self.predict_sales_forecast(product_line),
                'market_growth': self.predict_market_growth(product_line),
                'competitor_strategies': self.predict_competitor_strategy(competitors),
                'price_trends': self.predict_price_trends(product_line),
                'seasonal_analysis': self.analyze_seasonal_demand(product_line)
            }
            
            return forecast
        except Exception as e:
            print(f"Error generating comprehensive forecast: {e}")
            return {}

