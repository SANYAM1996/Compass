import os
import json
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


PROCESSED_DIR = "Data/Processed"
MODEL_DIR = "ML/models"
EVALUATION_DIR = "ML/evaluation"

RANDOM_STATE = 42


def load_processed_data():
    X_train = pd.read_csv(f"{PROCESSED_DIR}/X_train.csv")
    X_test = pd.read_csv(f"{PROCESSED_DIR}/X_test.csv")

    y_train = pd.read_csv(f"{PROCESSED_DIR}/y_complexity_train.csv").squeeze()
    y_test = pd.read_csv(f"{PROCESSED_DIR}/y_complexity_test.csv").squeeze()

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=8,
        min_samples_leaf=3,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)
    matrix = confusion_matrix(y_test, predictions)

    return accuracy, report, matrix, predictions


def save_outputs(model, accuracy, report, matrix, feature_names):
    os.makedirs(MODEL_DIR, exist_ok=True)
    os.makedirs(EVALUATION_DIR, exist_ok=True)

    joblib.dump(model, f"{MODEL_DIR}/complexity_model.pkl")

    metrics = {
        "model_name": "RandomForestClassifier",
        "accuracy": round(accuracy, 4),
        "classification_report": report,
        "confusion_matrix": matrix.tolist()
    }

    with open(f"{EVALUATION_DIR}/complexity_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    importance = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    importance.to_csv(f"{EVALUATION_DIR}/complexity_feature_importance.csv", index=False)

    print("Complexity model trained successfully.")
    print(f"Model saved to: {MODEL_DIR}/complexity_model.pkl")
    print(f"Metrics saved to: {EVALUATION_DIR}/complexity_metrics.json")
    print(f"Feature importance saved to: {EVALUATION_DIR}/complexity_feature_importance.csv")


def main():
    X_train, X_test, y_complexity_train, y_complexity_test = load_processed_data()

    model = train_model(X_train, y_complexity_train)

    accuracy, report, matrix, predictions = evaluate_model(model, X_test, y_complexity_test)

    save_outputs(
        model=model,
        accuracy=accuracy,
        report=report,
        matrix=matrix,
        feature_names=X_train.columns
    )

    print("\nAccuracy:", round(accuracy, 4))

    print("\nClassification Report:")
    print(classification_report(y_complexity_test, predictions))

    print("\nConfusion Matrix:")
    print(matrix)

    print("\nTop 10 Important Features:")
    importance = pd.DataFrame({
        "feature": X_train.columns,
        "importance": model.feature_importances_
    }).sort_values(by="importance", ascending=False)

    print(importance.head(10))


if __name__ == "__main__":
    main()