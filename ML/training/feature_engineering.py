import os

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder


DATA_PATH = "Data/Synthetic/onboarding_cases.csv"
PROCESSED_DIR = "Data/Processed"
MODEL_DIR = "ML/models"

RANDOM_STATE = 42
TEST_SIZE = 0.20

CATEGORICAL_COLUMNS = [
    "client_segment",
    "fund_type",
    "domicile",
    "aml_status",
    "kyc_status",
    "risk_rating",
    "client_priority",
    "latest_blocker_type",
]

BOOLEAN_COLUMNS = [
    "strategic_client",
]

NUMERIC_COLUMNS = [
    "num_sub_funds",
    "num_share_classes",
    "num_jurisdictions",
    "num_delegates",
    "missing_documents",
    "sla_days",
    "regulatory_review_required",
    "blocker_count",
]

TARGET_COLUMNS = [
    "complexity_label",
    "actual_effort_hours",
    "sla_breached",
]


def load_data(path: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

    required_columns = (
        CATEGORICAL_COLUMNS
        + BOOLEAN_COLUMNS
        + NUMERIC_COLUMNS
        + TARGET_COLUMNS
    )

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def build_features(df: pd.DataFrame):
    raw_features = df[
        CATEGORICAL_COLUMNS
        + BOOLEAN_COLUMNS
        + NUMERIC_COLUMNS
    ].copy()

    raw_features[BOOLEAN_COLUMNS] = (
        raw_features[BOOLEAN_COLUMNS]
        .astype(int)
    )

    encoder = OneHotEncoder(
        handle_unknown="ignore",
        sparse_output=False,
    )

    encoded_array = encoder.fit_transform(
        raw_features[CATEGORICAL_COLUMNS]
    )

    encoded_columns = encoder.get_feature_names_out(
        CATEGORICAL_COLUMNS
    )

    encoded_df = pd.DataFrame(
        encoded_array,
        columns=encoded_columns,
        index=raw_features.index,
    )

    features = pd.concat(
        [
            raw_features[NUMERIC_COLUMNS],
            raw_features[BOOLEAN_COLUMNS],
            encoded_df,
        ],
        axis=1,
    )

    targets = df[TARGET_COLUMNS].copy()

    return features, targets, encoder


def split_and_save():
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

    df = load_data()
    features, targets, encoder = build_features(df)

    train_indices, test_indices = train_test_split(
        df.index,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=targets["complexity_label"],
    )

    X_train = features.loc[train_indices].reset_index(drop=True)
    X_test = features.loc[test_indices].reset_index(drop=True)

    y_complexity_train = (
        targets.loc[train_indices, "complexity_label"]
        .reset_index(drop=True)
    )
    y_complexity_test = (
        targets.loc[test_indices, "complexity_label"]
        .reset_index(drop=True)
    )

    y_effort_train = (
        targets.loc[train_indices, "actual_effort_hours"]
        .reset_index(drop=True)
    )
    y_effort_test = (
        targets.loc[test_indices, "actual_effort_hours"]
        .reset_index(drop=True)
    )

    y_sla_train = (
        targets.loc[train_indices, "sla_breached"]
        .reset_index(drop=True)
    )
    y_sla_test = (
        targets.loc[test_indices, "sla_breached"]
        .reset_index(drop=True)
    )

    X_train.to_csv(
        f"{PROCESSED_DIR}/X_train.csv",
        index=False,
    )
    X_test.to_csv(
        f"{PROCESSED_DIR}/X_test.csv",
        index=False,
    )

    y_complexity_train.to_csv(
        f"{PROCESSED_DIR}/y_complexity_train.csv",
        index=False,
    )
    y_complexity_test.to_csv(
        f"{PROCESSED_DIR}/y_complexity_test.csv",
        index=False,
    )

    y_effort_train.to_csv(
        f"{PROCESSED_DIR}/y_effort_train.csv",
        index=False,
    )
    y_effort_test.to_csv(
        f"{PROCESSED_DIR}/y_effort_test.csv",
        index=False,
    )

    y_sla_train.to_csv(
        f"{PROCESSED_DIR}/y_sla_train.csv",
        index=False,
    )
    y_sla_test.to_csv(
        f"{PROCESSED_DIR}/y_sla_test.csv",
        index=False,
    )

    joblib.dump(
        encoder,
        f"{MODEL_DIR}/onehot_encoder.pkl",
    )

    joblib.dump(
        list(X_train.columns),
        f"{MODEL_DIR}/feature_columns.pkl",
    )

    print("Feature engineering completed.")
    print(f"X_train shape: {X_train.shape}")
    print(f"X_test shape: {X_test.shape}")
    print("All targets use the same train/test case split.")


if __name__ == "__main__":
    split_and_save()