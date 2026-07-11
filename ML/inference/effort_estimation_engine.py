def estimate_effort_hours(case: dict) -> dict:
    base_hours = 18

    effort = base_hours
    effort += case["num_sub_funds"] * 4
    effort += case["num_share_classes"] * 1.2
    effort += case["num_jurisdictions"] * 5
    effort += case["num_delegates"] * 4
    effort += case["missing_documents"] * 2.5
    effort += case["blocker_count"] * 8

    if case["aml_status"] == "In Progress":
        effort += 10
    elif case["aml_status"] == "Pending":
        effort += 18
    elif case["aml_status"] == "Blocked":
        effort += 30

    if case["kyc_status"] == "In Progress":
        effort += 8
    elif case["kyc_status"] == "Pending":
        effort += 16
    elif case["kyc_status"] == "Failed":
        effort += 28

    if case["risk_rating"] == "Medium":
        effort += 10
    elif case["risk_rating"] == "High":
        effort += 22

    if case["client_priority"] == "High":
        effort += 8
    elif case["client_priority"] == "Critical":
        effort += 15

    if case["regulatory_review_required"] == 1:
        effort += 14

    if case["strategic_client"]:
        effort += 12

    effort = round(effort, 1)
    effort_days = round(effort / 7.5, 1)

    if effort < 70:
        effort_band = "Low"
    elif effort < 130:
        effort_band = "Medium"
    else:
        effort_band = "High"

    return {
        "estimated_effort_hours": effort,
        "estimated_effort_days": effort_days,
        "effort_band": effort_band
    }


if __name__ == "__main__":
    sample_case = {
        "num_sub_funds": 12,
        "num_share_classes": 20,
        "num_jurisdictions": 4,
        "num_delegates": 5,
        "missing_documents": 8,
        "blocker_count": 2,
        "aml_status": "Pending",
        "kyc_status": "Completed",
        "risk_rating": "High",
        "client_priority": "Critical",
        "regulatory_review_required": 1,
        "strategic_client": True
    }

    print(estimate_effort_hours(sample_case))