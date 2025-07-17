import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def load_data(filepath):
    df = pd.read_csv(filepath)
    return df

def preprocess_data(df, target_column='Total'):
    df = df.copy()
    # Encode categorical columns
    label_encoders = {}
    for col in ['Branch', 'City', 'Customer type', 'Gender', 'Product line', 'Payment']:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    X = df.drop([target_column, 'Invoice ID', 'Date', 'Time'], axis=1)
    y = df[target_column]
    return X, y, label_encoders

def train_test_split_data(X, y, test_size=0.2, random_state=42):
    return train_test_split(X, y, test_size=test_size, random_state=random_state) 