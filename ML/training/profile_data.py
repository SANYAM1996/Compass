import os
import pandas as pd

DATA_PATH = "Data/Synthetic/onboarding_cases.csv"
OUTPUT_DIR = "ML/evaluation"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    print("\nDATASET SHAPE")
    print(df.shape)

    print("\nCOLUMNS")
    print(df.columns.tolist())

    print("\nCOMPLEXITY DISTRIBUTION")
    print(df["complexity_label"].value_counts(normalize=True).round(3))

    print("\nPRESSURE BAND DISTRIBUTION")
    print(df["pressure_band"].value_counts(normalize=True).round(3))

    print("\nSLA BREACH RATE")
    print(df["sla_breached"].value_counts(normalize=True).round(3))

    print("\nAVERAGE EFFORT BY COMPLEXITY")
    print(df.groupby("complexity_label")["actual_effort_hours"].mean().round(1))

    print("\nAVERAGE OPS BY CLIENT")
    print(
        df.groupby("client_name")["operational_pressure_score"]
        .mean()
        .sort_values(ascending=False)
        .head(15)
        .round(1)
    )

    print("\nHIGH PROFILE CLIENT COMPLEXITY")
    print(
        df[df["strategic_client"] == True]
        .groupby("client_name")["complexity_label"]
        .value_counts(normalize=True)
        .round(3)
    )

    summary_path = f"{OUTPUT_DIR}/data_profile_summary.csv"

    summary = df.describe(include="all").transpose()
    summary.to_csv(summary_path)

    print(f"\nSaved summary to: {summary_path}")


if __name__ == "__main__":
    main()