from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from ML.inference.effort_estimation_engine import estimate_effort_hours
from ML.inference.recommendation_engine import recommend_analysts


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_PATH = PROJECT_ROOT / "ML" / "models" / "complexity_model.pkl"
ENCODER_PATH = PROJECT_ROOT / "ML" / "models" / "onehot_encoder.pkl"
FEATURE_COLUMNS_PATH = PROJECT_ROOT / "ML" / "models" / "feature_columns.pkl"


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

BOOLEAN_COLUMNS = [
    "strategic_client",
]


model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)
feature_columns = joblib.load(FEATURE_COLUMNS_PATH)


def prepare_features(case: dict[str, Any]) -> pd.DataFrame:
    case_df = pd.DataFrame([case])

    case_df[BOOLEAN_COLUMNS] = (
        case_df[BOOLEAN_COLUMNS]
        .astype(int)
    )

    encoded_array = encoder.transform(
        case_df[CATEGORICAL_COLUMNS]
    )

    encoded_df = pd.DataFrame(
        encoded_array,
        columns=encoder.get_feature_names_out(
            CATEGORICAL_COLUMNS
        ),
        index=case_df.index,
    )

    features = pd.concat(
        [
            case_df[NUMERIC_COLUMNS],
            case_df[BOOLEAN_COLUMNS],
            encoded_df,
        ],
        axis=1,
    )

    features = features.reindex(
        columns=feature_columns,
        fill_value=0,
    )

    return features


def dataframe_to_records(
    dataframe: pd.DataFrame,
) -> list[dict[str, Any]]:
    records = dataframe.to_dict(orient="records")

    for record in records:
        for key, value in record.items():
            if hasattr(value, "item"):
                record[key] = value.item()

    return records


def predict_case(case: dict[str, Any]) -> dict[str, Any]:
    features = prepare_features(case)

    predicted_complexity = str(
        model.predict(features)[0]
    )

    probabilities = model.predict_proba(features)[0]
    best_probability_index = probabilities.argmax()

    confidence = float(
        probabilities[best_probability_index] * 100
    )

    effort_estimate = estimate_effort_hours(case)

    recommendations = recommend_analysts(
        case=case,
        complexity_label=predicted_complexity,
        top_n=5,
    )

    recommendation_records = dataframe_to_records(
        recommendations
    )



    eligible_records = [
    analyst
    for analyst in recommendation_records
    if analyst["eligibility_status"]
    == "Eligible"
]

    recommended_analyst = (
    eligible_records[0]
    if eligible_records
    else None
)

    allocation_status = (
    "Recommendation Available"
    if recommended_analyst
    else "Manager Review Required"
)





















    return {
        "predicted_complexity":
            predicted_complexity,
        "prediction_confidence":
            round(confidence, 2),
        "estimated_effort":
            effort_estimate,
        "allocation_status":
            allocation_status,
        "recommended_analyst":
            recommended_analyst,
        "top_recommendations":
            recommendation_records,
}