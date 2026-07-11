import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

N_CASES = 5000

HIGH_PROFILE_CLIENTS = ["Aon", "RiverRock", "Apollo", "Varagon Generation"]

MEDIUM_CLIENTS = [
    "BlackRock", "State Street", "J.P. Morgan", "Goldman Sachs", "BNY",
    "Northern Trust", "PIMCO", "Schroders", "Fidelity", "M&G",
    "Legal & General", "Invesco", "Abrdn", "AllianzGI", "DWS"
]

SMALL_CLIENTS = [
    "Emerald Capital", "Blue Horizon", "OakBridge", "SilverStone",
    "Nova Asset Management", "Celtic Investments", "Harbour Capital",
    "GreenRock", "Evercrest", "NorthPeak", "Liffey Investments",
    "Arbour Wealth"
]

ANALYSTS = [
    ("A001", "John Murphy", "Manager", 9, ["UCITS", "Regulatory", "KYC"]),
    ("A002", "Sarah O'Connor", "Senior Associate", 7, ["AML", "KYC", "UCITS", "Regulatory"]),
    ("A003", "Emma Walsh", "Assistant Manager", 8, ["Private Equity", "Real Estate", "Regulatory"]),
    ("A004", "David Byrne", "Senior Associate", 6, ["Hedge Fund", "AIF", "AML"]),
    ("A005", "Mark Kelly", "Associate", 3, ["KYC", "UCITS"]),
    ("A006", "Aoife Brennan", "Senior Associate", 6, ["AML", "Regulatory"]),
    ("A007", "Michael Doyle", "Manager", 10, ["Complex Structures", "AIF", "Regulatory"]),
    ("A008", "Niamh Ryan", "Associate", 4, ["UCITS", "KYC"]),
    ("A009", "Conor Flynn", "Senior Associate", 5, ["Hedge Fund", "AML"]),
    ("A010", "Laura Hughes", "Assistant Manager", 8, ["Regulatory", "AML", "AIF"]),
    ("A011", "Patrick Nolan", "Senior Associate", 6, ["AIF", "Private Equity"]),
    ("A012", "Rachel McCarthy", "Associate", 3, ["KYC", "AML"]),
    ("A013", "Brian O'Sullivan", "Manager", 11, ["UCITS", "Complex Structures", "Regulatory", "AML"]),
    ("A014", "James Fitzgerald", "Associate", 2, ["UCITS", "KYC"]),
    ("A015", "Sophie Bennett", "Senior Associate", 5, ["Real Estate", "Private Equity"]),
    ("A016", "Daniel Clarke", "Assistant Manager", 7, ["Hedge Fund", "AIF"]),
    ("A017", "Emily Thompson", "Associate", 4, ["AML", "KYC"]),
    ("A018", "Kevin Reilly", "Senior Associate", 6, ["Regulatory", "UCITS"]),
]

FUND_TYPES = ["UCITS", "AIF", "Hedge Fund", "Private Equity", "Real Estate", "Money Market"]
DOMICILES = ["Ireland", "Luxembourg", "UK", "Cayman Islands", "Malta"]
AML_STATUSES = ["Completed", "In Progress", "Pending", "Blocked"]
KYC_STATUSES = ["Completed", "In Progress", "Pending", "Failed"]
RISK_RATINGS = ["Low", "Medium", "High"]
PRIORITIES = ["Low", "Normal", "High", "Critical"]


def weighted_choice(options, weights):
    return random.choices(options, weights=weights, k=1)[0]


def generate_analysts():
    rows = []

    for analyst_id, name, seniority, experience, skills in ANALYSTS:
        workload = np.random.randint(35, 92)

        rows.append({
            "analyst_id": analyst_id,
            "analyst_name": name,
            "seniority": seniority,
            "experience_years": experience,
            "team": weighted_choice(
                ["Client Onboarding", "AML Operations", "Dublin Operations", "Luxembourg Operations"],
                [0.45, 0.25, 0.2, 0.1]
            ),
            "skills": ",".join(skills),
            "capacity_hours_per_week": 37.5,
            "current_workload_pct": workload,
            "available_hours": round(37.5 * (1 - workload / 100), 1),
            "active_cases": np.random.randint(2, 12),
            "avg_completion_quality": round(np.random.uniform(3.6, 5.0), 2),
            "availability_status": weighted_choice(
                ["Available", "Limited", "Unavailable"],
                [0.75, 0.18, 0.07]
            )
        })

    return pd.DataFrame(rows)


def choose_client():
    client_group = weighted_choice(
        ["high", "medium", "small"],
        [0.18, 0.52, 0.30]
    )

    if client_group == "high":
        return random.choice(HIGH_PROFILE_CLIENTS), "High Profile", True

    if client_group == "medium":
        return random.choice(MEDIUM_CLIENTS), "Institutional", False

    return random.choice(SMALL_CLIENTS), "Small / Emerging", False


def calculate_complexity(row):
    score = 0

    score += row["num_sub_funds"] * 2.2
    score += row["num_share_classes"] * 0.8
    score += row["num_jurisdictions"] * 4.5
    score += row["num_delegates"] * 3.5
    score += row["missing_documents"] * 2.3
    score += row["blocker_count"] * 8

    if row["aml_status"] == "In Progress":
        score += 8
    elif row["aml_status"] == "Pending":
        score += 15
    elif row["aml_status"] == "Blocked":
        score += 28

    if row["kyc_status"] == "In Progress":
        score += 7
    elif row["kyc_status"] == "Pending":
        score += 14
    elif row["kyc_status"] == "Failed":
        score += 25

    if row["risk_rating"] == "Medium":
        score += 10
    elif row["risk_rating"] == "High":
        score += 25

    if row["client_priority"] == "High":
        score += 8
    elif row["client_priority"] == "Critical":
        score += 16

    if row["fund_type"] in ["Hedge Fund", "Private Equity", "Real Estate"]:
        score += 12

    if row["regulatory_review_required"] == 1:
        score += 12

    if row["strategic_client"]:
        score += 15

    return round(score, 1)


def complexity_label(score):
    if score < 75:
        return "Low"
    elif score < 125:
        return "Medium"
    return "High"


def pressure_band(score):
    if score < 40:
        return "Low"
    elif score < 65:
        return "Medium"
    elif score < 85:
        return "High"
    return "Critical"


def calculate_ops(row):
    ops = 0

    ops += min(row["complexity_score"] * 0.45, 45)

    if row["sla_days"] <= 10:
        ops += 20
    elif row["sla_days"] <= 20:
        ops += 12
    else:
        ops += 5

    if row["strategic_client"]:
        ops += 12

    if row["aml_status"] in ["Pending", "Blocked"]:
        ops += 10

    if row["kyc_status"] in ["Pending", "Failed"]:
        ops += 10

    ops += row["blocker_count"] * 3

    return min(round(ops, 1), 100)


def generate_cases():
    rows = []

    for i in range(1, N_CASES + 1):
        client_name, client_segment, strategic_client = choose_client()

        if strategic_client:
            fund_type = weighted_choice(FUND_TYPES, [0.25, 0.2, 0.15, 0.2, 0.15, 0.05])
            num_sub_funds = np.random.randint(8, 26)
            num_share_classes = np.random.randint(10, 45)
            num_jurisdictions = np.random.randint(3, 8)
            num_delegates = np.random.randint(3, 10)
            missing_documents = np.random.randint(4, 22)
            aml_status = weighted_choice(AML_STATUSES, [0.25, 0.35, 0.25, 0.15])
            kyc_status = weighted_choice(KYC_STATUSES, [0.25, 0.35, 0.25, 0.15])
            risk_rating = weighted_choice(RISK_RATINGS, [0.10, 0.35, 0.55])
            priority = weighted_choice(PRIORITIES, [0.02, 0.13, 0.45, 0.40])
            sla_days = weighted_choice([10, 15, 20, 30, 45], [0.25, 0.35, 0.25, 0.10, 0.05])
            blocker_count = np.random.randint(1, 6)
        else:
            fund_type = random.choice(FUND_TYPES)
            num_sub_funds = np.random.randint(1, 16)
            num_share_classes = np.random.randint(1, 30)
            num_jurisdictions = np.random.randint(1, 6)
            num_delegates = np.random.randint(0, 7)
            missing_documents = np.random.randint(0, 16)
            aml_status = weighted_choice(AML_STATUSES, [0.45, 0.30, 0.18, 0.07])
            kyc_status = weighted_choice(KYC_STATUSES, [0.45, 0.30, 0.18, 0.07])
            risk_rating = weighted_choice(RISK_RATINGS, [0.35, 0.45, 0.20])
            priority = weighted_choice(PRIORITIES, [0.15, 0.55, 0.25, 0.05])
            sla_days = weighted_choice([10, 15, 20, 30, 45], [0.08, 0.18, 0.28, 0.30, 0.16])
            blocker_count = np.random.randint(0, 4)

        row = {
            "case_id": f"C{i:05}",
            "client_name": client_name,
            "client_segment": client_segment,
            "strategic_client": strategic_client,
            "fund_type": fund_type,
            "domicile": random.choice(DOMICILES),
            "num_sub_funds": num_sub_funds,
            "num_share_classes": num_share_classes,
            "num_jurisdictions": num_jurisdictions,
            "num_delegates": num_delegates,
            "missing_documents": missing_documents,
            "aml_status": aml_status,
            "kyc_status": kyc_status,
            "risk_rating": risk_rating,
            "client_priority": priority,
            "sla_days": sla_days,
            "regulatory_review_required": weighted_choice([0, 1], [0.65, 0.35 if strategic_client else 0.20]),
            "blocker_count": blocker_count,
            "latest_blocker_type": weighted_choice(
                ["None", "AML Delay", "KYC Issue", "Missing Documents", "Regulatory Review", "Analyst Unavailable", "Client Dependency"],
                [0.45, 0.14, 0.12, 0.12, 0.08, 0.04, 0.05]
            )
        }

        score = calculate_complexity(row)
        row["complexity_score"] = score
        row["complexity_label"] = complexity_label(score)

        effort_hours = score * np.random.uniform(0.72, 1.18) + np.random.normal(6, 4)
        row["actual_effort_hours"] = round(max(6, effort_hours), 1)
        row["actual_completion_days"] = round(row["actual_effort_hours"] / 7.5 + np.random.uniform(1, 5), 1)
       





        ops = calculate_ops(row)
        row["operational_pressure_score"] = ops
        row["pressure_band"] = pressure_band(ops)
        breach_probability = 0.05

        if row["complexity_label"] == "Medium":
         breach_probability += 0.08

        if row["complexity_label"] == "High":
            breach_probability += 0.15

        if row["operational_pressure_score"] > 80:
            breach_probability += 0.10

        if row["client_priority"] == "Critical":
            breach_probability += 0.06

        if row["blocker_count"] >= 3:
            breach_probability += 0.08

        breach_probability = min(breach_probability, 0.35)

        row["sla_breached"] = int(np.random.random() < breach_probability)


        rows.append(row)

    return pd.DataFrame(rows)


def generate_allocation_history(cases, analysts):
    rows = []

    for _, case in cases.iterrows():
        available = analysts[analysts["availability_status"] != "Unavailable"]

        if case["complexity_label"] == "High":
            pool = available[available["experience_years"] >= 6]
            if pool.empty:
                pool = available
        else:
            pool = available

        analyst = pool.sample(1).iloc[0]

        rows.append({
            "case_id": case["case_id"],
            "analyst_id": analyst["analyst_id"],
            "analyst_name": analyst["analyst_name"],
            "assigned_date": datetime.today() - timedelta(days=np.random.randint(1, 365)),
            "allocation_status": weighted_choice(
                ["Completed", "Delayed", "Escalated"],
                [0.72, 0.18, 0.10]
            ),
            "manager_override": weighted_choice([0, 1], [0.82, 0.18])
        })

    return pd.DataFrame(rows)


def main():
    output_dir = "Data/Synthetic"
    os.makedirs(output_dir, exist_ok=True)

    analysts = generate_analysts()
    cases = generate_cases()
    allocation_history = generate_allocation_history(cases, analysts)

    analysts.to_csv(f"{output_dir}/analysts.csv", index=False)
    cases.to_csv(f"{output_dir}/onboarding_cases.csv", index=False)
    allocation_history.to_csv(f"{output_dir}/allocation_history.csv", index=False)

    print("Synthetic data generated successfully.")
    print(f"Cases: {len(cases)}")
    print(f"Analysts: {len(analysts)}")
    print(f"Allocation history: {len(allocation_history)}")
    print("\nComplexity distribution:")
    print(cases["complexity_label"].value_counts())
    print("\nTop high-pressure clients:")
    print(cases.groupby("client_name")["operational_pressure_score"].mean().sort_values(ascending=False).head(10))


if __name__ == "__main__":
    main()