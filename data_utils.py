import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

def load_data(filepath):
    """Load data from CSV or Excel file"""
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    return df

def detect_columns(df):
    """Automatically detect important columns in the dataset"""
    date_col = None
    target_col = None
    product_col = None
    external_cols = []
    
    # Detect date column
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['date', 'time', 'timestamp']):
            date_col = col
            break
    
    # Detect target column (sales, total, profit, revenue)
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['sales', 'total', 'profit', 'revenue', 'amount']):
            if pd.api.types.is_numeric_dtype(df[col]):
                target_col = col
                break
    
    # Detect product column
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['product', 'item', 'category', 'line']):
            product_col = col
            break
    
    # Detect external factors
    for col in df.columns:
        if any(keyword in col.lower() for keyword in ['weather', 'event', 'crisis', 'season', 'holiday']):
            external_cols.append(col)
    
    return date_col, target_col, product_col, external_cols

def preprocess_dynamic(df, date_col, target_col, product_col, external_cols):
    """Preprocess data dynamically based on detected columns"""
    df = df.copy()
    
    # Handle date columns
    if date_col and date_col in df.columns:
        try:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            df['Year'] = df[date_col].dt.year
            df['Month'] = df[date_col].dt.month
            df['DayOfWeek'] = df[date_col].dt.dayofweek
            df['Quarter'] = df[date_col].dt.quarter
        except:
            pass
    
    # Handle categorical columns
    label_encoders = {}
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    for col in categorical_cols:
        if col not in [target_col, date_col] and not col.lower().endswith('id'):
            try:
                # Use pandas factorize for simple encoding
                df[col], unique_vals = pd.factorize(df[col])
                label_encoders[col] = unique_vals
            except:
                pass
    
    # Select feature columns
    feature_cols = []
    for col in df.columns:
        if (col != target_col and 
            col != date_col and 
            not col.lower().endswith('id') and
            pd.api.types.is_numeric_dtype(df[col])):
            feature_cols.append(col)
    
    # Handle missing values
    df = df.fillna(0)
    
    # Prepare features and target
    if feature_cols:
        X = df[feature_cols]
    else:
        X = pd.DataFrame()
    
    y = df[target_col] if target_col and target_col in df.columns else pd.Series()
    
    return X, y, label_encoders, feature_cols

def prepare_forecast_data(df, target_col, periods=30):
    """Prepare data for forecasting"""
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in data")
    
    # Sort by date if available
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    if date_cols:
        df = df.sort_values(date_cols[0])
    
    # Get target series
    y = df[target_col].dropna()
    
    return y

def validate_data(df):
    """Validate uploaded data"""
    errors = []
    warnings = []
    
    # Check if dataframe is empty
    if df.empty:
        errors.append("The uploaded file is empty")
        return errors, warnings
    
    # Check minimum rows
    if len(df) < 10:
        warnings.append("Dataset has fewer than 10 rows. Results may be unreliable.")
    
    # Check for numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) == 0:
        errors.append("No numeric columns found in the data")
    
    # Check for missing values
    missing_pct = (df.isnull().sum() / len(df)) * 100
    high_missing = missing_pct[missing_pct > 50]
    if len(high_missing) > 0:
        warnings.append(f"Columns with >50% missing values: {list(high_missing.index)}")
    
    return errors, warnings
