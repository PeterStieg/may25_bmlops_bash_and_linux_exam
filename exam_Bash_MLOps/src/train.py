"""
-------------------------------------------------------------------------------
This script runs the training of an XGBoost model to predict graphics card processed
from the processed data.

1. It starts by searching for the latest processed CSV file in the 'data/processed/' directory.
2. If a standard model (model.pkl) does not exist, it loads the data, splits it into training and test sets, trains a model on this data, evaluates it, and then saves it as 'model/model.pkl'.
3. If a standard model already exists, it trains a new model on the latest data, evaluates it, and saves the model in the 'model/' folder in the format: model_YYYYMMDD_HHMM.pkl.
4. Performance metrics (RMSE, MAE, R²) are displayed and saved in the log file.
5. Any errors are handled and reported in the logs.

The models are saved in the 'model/' folder with the name 'model.pkl' for the standard model and with a timestamp for later versions.
The model metrics are recorded in the script’s log files.
-------------------------------------------------------------------------------
"""

import os
import pickle

import numpy as np
import pandas as pd
import xgboost as xgb

from datetime import datetime, timezone
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# 1. Get latest processed CSV file
def get_latest_processed_file(processed_data_path="../data/processed/"):
    """Get the latest processed CSV file."""
    processed_data_all_files = os.listdir(processed_data_path)
    processed_data_csv_files = [
        os.path.join(processed_data_path, x)
        for x in processed_data_all_files
        if x.endswith(".csv")
    ]

    latest_file = max(processed_data_csv_files, key=os.path.getmtime)

    return latest_file


def load_and_prepare_data(file_path):
    """Load and prepare CSV file in DataFrame for training."""

    # Load the CSV data
    df = pd.read_csv(file_path)

    # Encode graphics card model names
    label_encoder = LabelEncoder()
    df["model_encoded"] = label_encoder.fit_transform(df["model"])

    # Prepare features and target
    features = ["year", "month", "day_of_year", "model_encoded"]
    X = df[features]
    y = df["sales"]

    return X, y, label_encoder


# 5. Log erros
def log_errors(timestamp_basic, e):
    """
    Task 5: Any errors are handled and reported in the logs.
    """

    log_file_path = "../logs/errors.logs"
    log_file_header = "timestamp;error\n"

    # Check if the log file exist, if not create it and write header
    # Check if the log file is empty, if so, write the header
    if (not os.path.exists(log_file_path)) or (os.path.getsize(log_file_path) == 0):
        with open(log_file_path, "w") as log_file:
            log_file.write(log_file_header)

    with open(log_file_path, "a") as log_file:
        log_file.write(f"{timestamp_basic};{e}\n")


# 4. Performance metrics are displayed and saved in the log file: RMSE, MAE, R²
def display_and_save_metrics(metrics, model_path, timestamp_basic):
    """
    Task 4: Display performance metrics (RMSE, MAE, R²) and save them to log file.
    """

    log_file_path = "../logs/train.logs"
    log_file_header = "timestamp;model_path;rmse;mae;r2\n"

    # Check if the log file exist, if not create it and write header
    # Check if the log file is empty, if so, write the header
    if (not os.path.exists(log_file_path)) or (os.path.getsize(log_file_path) == 0):
        with open(log_file_path, "w") as log_file:
            log_file.write(log_file_header)

    with open(log_file_path, "a") as log_file:
        log_file.write(
            f"{timestamp_basic};{model_path};{metrics['RMSE']:.6f};{metrics['MAE']:.6f};{metrics['R²']:.6f}\n"
        )


def calculate_metrics(y_true, y_pred):
    """Calculate performance metrics."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {"RMSE": rmse, "MAE": mae, "R²": r2}


# 2. & 3. Train model: Load data, split into training/test sets, train model, evaluate
def train_model(X, y):
    """Load data, split into training/test sets, train model, evaluate."""

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train XGBoost model
    model = xgb.XGBRegressor(
        n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42, n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    metrics = calculate_metrics(y_test, y_pred)

    return model, metrics


# 2. & 3. Save model
# If standard model does not exist, save as 'model.pkl'
# else save as 'model_YYYYMMDD_HHMM.pkl'
def save_model(model, label_encoder, metrics, timestamp_basic):
    """Save the first model as 'model/model.pkl'."""

    os.makedirs("model", exist_ok=True)

    standard_model_exists = os.path.exists(model_path)

    if not standard_model_exists:
        # Save the model as 'model.pkl'
        model_path = "../model/model.pkl"
    else:
        model_path = f"../model/model_{timestamp_basic}.pkl"

    encoder_path = "../model/label_encoder.pkl"

    # Save model and encoder
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    with open(encoder_path, "wb") as f:
        pickle.dump(label_encoder, f)

    # Display and save metrics
    display_and_save_metrics(metrics, model_path, timestamp_basic)

    return model_path  # To-Do: Is this necessary?


def main():
    """
    Main function that orchestrates tasks in the correct order.
    """

    timestamp_basic = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    try:
        # TASK 1: Get latest processed CSV file
        data_file = get_latest_processed_file()

        # Load and prepare data for training
        X, y, label_encoder = load_and_prepare_data(data_file)

        # TASK 2 & 3: Train model

        model, metrics = train_model(X, y)
        save_model(model, label_encoder, metrics, timestamp_basic)

    except Exception as e:
        print(f"Training pipeline failed: {e}")
        log_errors(timestamp_basic, e)
        raise


if __name__ == "__main__":
    main()
