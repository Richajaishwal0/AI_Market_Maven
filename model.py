import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

def simple_forecast(y, periods, method='moving_average'):
    """
    Generate simple forecasts using statistical methods
    
    Parameters:
    - y: pandas Series of historical values
    - periods: number of periods to forecast
    - method: forecasting method ('moving_average', 'exponential', 'linear_trend')
    """
    if len(y) == 0:
        return np.zeros(periods)
    
    # Clean the data
    y = y.dropna()
    
    if len(y) == 0:
        return np.zeros(periods)
    
    if method == 'moving_average':
        # Use moving average of last N periods
        window = min(30, len(y))
        forecast_value = y.rolling(window=window, min_periods=1).mean().iloc[-1]
        
        # Add slight trend if detectable
        if len(y) >= 2:
            recent_trend = (y.iloc[-1] - y.iloc[-min(10, len(y))]) / min(10, len(y))
            forecast_values = []
            for i in range(periods):
                forecast_values.append(forecast_value + (recent_trend * i))
        else:
            forecast_values = [forecast_value] * periods
            
    elif method == 'exponential':
        # Exponential smoothing
        alpha = 0.3
        forecast_value = y.iloc[0]
        
        for value in y:
            forecast_value = alpha * value + (1 - alpha) * forecast_value
        
        # Simple exponential forecast
        forecast_values = [forecast_value] * periods
        
    elif method == 'linear_trend':
        # Linear trend forecast
        if len(y) >= 2:
            x = np.arange(len(y)).reshape(-1, 1)
            model = LinearRegression()
            model.fit(x, y)
            
            # Predict future periods
            future_x = np.arange(len(y), len(y) + periods).reshape(-1, 1)
            forecast_values = model.predict(future_x)
        else:
            forecast_values = [y.iloc[0]] * periods
    
    else:
        # Default to mean
        forecast_values = [y.mean()] * periods
    
    # Ensure positive values
    forecast_values = np.maximum(forecast_values, 0)
    
    # Add some realistic variation
    std_dev = y.std() * 0.1  # 10% of standard deviation
    noise = np.random.normal(0, std_dev, periods)
    forecast_values = forecast_values + noise
    forecast_values = np.maximum(forecast_values, 0)  # Keep positive
    
    return forecast_values

def train_advanced_model(X, y, model_type='random_forest'):
    """Train an advanced ML model"""
    if model_type == 'random_forest':
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
    elif model_type == 'linear':
        model = LinearRegression()
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X, y)
    return model

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    predictions = model.predict(X_test)
    
    metrics = {
        'MAE': mean_absolute_error(y_test, predictions),
        'MSE': mean_squared_error(y_test, predictions),
        'RMSE': np.sqrt(mean_squared_error(y_test, predictions)),
        'R2': r2_score(y_test, predictions)
    }
    
    return metrics, predictions

def save_model(model, filepath):
    """Save trained model"""
    joblib.dump(model, filepath)

def load_model(filepath):
    """Load saved model"""
    return joblib.load(filepath)

def forecast_with_confidence(y, periods, confidence_level=0.95):
    """Generate forecast with confidence intervals"""
    forecast = simple_forecast(y, periods)
    
    # Calculate confidence intervals based on historical volatility
    std_dev = y.std()
    z_score = 1.96 if confidence_level == 0.95 else 2.58  # 95% or 99%
    
    margin_of_error = z_score * std_dev
    
    upper_bound = forecast + margin_of_error
    lower_bound = forecast - margin_of_error
    lower_bound = np.maximum(lower_bound, 0)  # Keep positive
    
    return {
        'forecast': forecast,
        'upper_bound': upper_bound,
        'lower_bound': lower_bound,
        'confidence_level': confidence_level
    }

def detect_seasonality(y, freq='monthly'):
    """Detect seasonal patterns in the data"""
    if len(y) < 24:  # Need at least 2 years of monthly data
        return None
    
    # Simple seasonal decomposition
    if freq == 'monthly':
        season_length = 12
    elif freq == 'weekly':
        season_length = 52
    else:
        season_length = 4  # quarterly
    
    if len(y) < season_length * 2:
        return None
    
    # Calculate seasonal indices
    seasonal_data = []
    for i in range(season_length):
        season_values = y[i::season_length]
        seasonal_data.append(season_values.mean())
    
    return seasonal_data

def trend_analysis(y):
    """Analyze trend in the data"""
    if len(y) < 3:
        return {'trend': 'insufficient_data', 'slope': 0}
    
    x = np.arange(len(y))
    slope, intercept = np.polyfit(x, y, 1)
    
    if slope > 0:
        trend = 'increasing'
    elif slope < 0:
        trend = 'decreasing'
    else:
        trend = 'stable'
    
    return {
        'trend': trend,
        'slope': slope,
        'intercept': intercept,
        'change_rate': (slope / y.mean()) * 100 if y.mean() != 0 else 0
    }
