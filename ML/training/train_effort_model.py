import os
import json
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


PROCESSED_DIR = "Data/Processed"
MODEL_DIR = "ML/models"
EVALUATION_DIR = "ML/evaluation"

RANDOM_STATE = 42


def load_processed_data():
    X_train = pd.read_csv(f"{PROCESSED_DIR}/X_train.csv")
    X_test = pd.read_csv(f"{PROCESSED_DIR}/X_test.csv")

    y_train = pd.read_csv(f"{PROCESSED_DIR}/y_effort_train.csv").squeeze()
    y_test = pd.read_csv(f"{PROCESSED_DIR}/y_effort_test.csv").squeeze()

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=14,
        min_samples_split=8,
        min_samples_leaf=3,
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = mse ** 0.5
    r2 = r2_score(y_test, predictions)

    return mae, rmse, r2, predictions


def save_outputs(model, mae, rmse, r2, feature_names):
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(EVALUATION_DIR, exist_ok=True)

    joblib.dump(model, f"{MODEL_DIR}/effort_model.pkl")

    metrics = {
        "model_name": "RandomForestRegressor",
        "mae": round(mae, 2),
        "rmse": round(rmse, 2),
        "r2_score": round(r2, 4)
    }

    with open(f"{EVALUATION_DIR}/effort_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    importance.to_csv(f"{EVALUATION_DIR}/effort_feature_importance.csv", index=False)

    print("Effort model trained successfully.")
    print(f"Model saved to: {MODEL_DIR}/effort_model.pkl")
    print(f"Metrics saved to: {EVALUATION_DIR}/effort_metrics.json")
    print(f"Feature importance saved to: {EVALUATION_DIR}/effort_feature_importance.csv")


def main():
    X_train, X_test, y_effort_train, y_effort_test = load_processed_data()

    model = train_model(X_train, y_effort_train)

    mae, rmse, r2, predictions = evaluate_model(model, X_test, y_effort_test)

    save_outputs(
        model=model,
        mae=mae,
        rmse=rmse,
        r2=r2,
        feature_names=X_train.columns
    )

    print("\nMAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))

    print("\nSample Predictions:")
    sample = pd.DataFrame({
        "Actual Effort Hours": y_effort_test.head(10).values,
        "Predicted Effort Hours": predictions[:10].round(1)
    })

    print(sample)

    print("\nTop 10 Important Features:")
    importance = pd.DataFrame({
        "feature": X_train.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    print(importance.head(10))


if __name__ == "__main__":
    main()