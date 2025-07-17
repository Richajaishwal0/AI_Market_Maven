from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = mse ** 0.5  # Compute RMSE manually for compatibility
    return {'MAE': mae, 'MSE': mse, 'RMSE': rmse}

def save_model(model, path):
    joblib.dump(model, path)

def load_model(path):
    return joblib.load(path) 