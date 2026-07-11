import pandas as pd


ANALYSTS_PATH = "Data/Synthetic/analysts.csv"


REQUIRED_SKILLS_BY_CASE = {
    "UCITS": ["UCITS"],
    "AIF": ["AIF"],
    "Hedge Fund": ["Hedge Fund"],
    "Private Equity": ["Private Equity"],
    "Real Estate": ["Real Estate"],
    "Money Market": ["UCITS"],
}


def load_analysts(path: str = ANALYSTS_PATH) -> pd.DataFrame:
    return pd.read_csv(path)


def get_required_skills(case: dict) -> list[str]:
    required_skills = []

    required_skills.extend(
        REQUIRED_SKILLS_BY_CASE.get(case["fund_type"], [])
    )

    if case["aml_status"] in ["In Progress", "Pending", "Blocked"]:
        required_skills.append("AML")

    if case["kyc_status"] in ["In Progress", "Pending", "Failed"]:
        required_skills.append("KYC")

    if case["regulatory_review_required"] == 1:
        required_skills.append("Regulatory")

    if (
        case["num_sub_funds"] >= 10
        or case["num_delegates"] >= 5
    ):
        required_skills.append("Complex Structures")

    return list(set(required_skills))


def get_mandatory_skills(case: dict) -> list[str]:
    mandatory_skills = []

    if case["aml_status"] in ["Pending", "Blocked"]:
        mandatory_skills.append("AML")

    if case["kyc_status"] in ["Pending", "Failed"]:
        mandatory_skills.append("KYC")

    if case["regulatory_review_required"] == 1:
        mandatory_skills.append("Regulatory")

    if case["fund_type"] in [
        "UCITS",
        "AIF",
        "Hedge Fund",
        "Private Equity",
        "Real Estate",
    ]:
        mandatory_skills.append(case["fund_type"])

    if (
        case["num_sub_funds"] >= 15
        or case["num_delegates"] >= 7
    ):
        mandatory_skills.append("Complex Structures")

    return list(set(mandatory_skills))


def calculate_skill_score(
    required_skills: list[str],
    analyst_skills: list[str],
) -> tuple[float, list[str]]:
    if not required_skills:
        return 40.0, []

    matched_skills = [
        skill
        for skill in required_skills
        if skill in analyst_skills
    ]

    score = round(
        len(matched_skills) / len(required_skills) * 40,
        1,
    )

    return score, matched_skills


def calculate_workload_score(workload_pct: float) -> float:
    if workload_pct >= 95:
        return 0.0

    return round(
        max(0, (100 - workload_pct) / 100 * 25),
        1,
    )


def calculate_experience_score(
    experience_years: float,
    complexity_label: str,
) -> float:
    if complexity_label == "High":
        return round(
            min(experience_years / 10 * 15, 15),
            1,
        )

    if complexity_label == "Medium":
        return round(
            min(experience_years / 7 * 15, 15),
            1,
        )

    return round(
        min(experience_years / 4 * 15, 15),
        1,
    )


def calculate_availability_score(status: str) -> float:
    if status == "Available":
        return 10.0

    if status == "Limited":
        return 5.0

    return 0.0


def calculate_quality_score(avg_quality: float) -> float:
    return round(
        avg_quality / 5 * 10,
        1,
    )


def generate_reasons(
    analyst: pd.Series,
    required_skills: list[str],
    matched_skills: list[str],
    missing_mandatory_skills: list[str],
) -> list[str]:
    reasons = []

    if matched_skills:
        reasons.append(
            f"Matches required skills: {', '.join(matched_skills)}"
        )

    if analyst["current_workload_pct"] < 65:
        reasons.append(
            f"Healthy workload at "
            f"{analyst['current_workload_pct']}%"
        )
    elif analyst["current_workload_pct"] < 85:
        reasons.append(
            f"Manageable workload at "
            f"{analyst['current_workload_pct']}%"
        )
    else:
        reasons.append(
            f"High workload at "
            f"{analyst['current_workload_pct']}%"
        )

    if analyst["availability_status"] == "Available":
        reasons.append("Available for allocation")
    elif analyst["availability_status"] == "Limited":
        reasons.append("Limited availability")
    else:
        reasons.append("Currently unavailable")

    reasons.append(
        f"{analyst['experience_years']} years of experience"
    )

    reasons.append(
        f"Quality score "
        f"{analyst['avg_completion_quality']}/5"
    )

    missing_preferred_skills = [
        skill
        for skill in required_skills
        if skill not in matched_skills
    ]

    if missing_preferred_skills:
        reasons.append(
            "Missing preferred skills: "
            f"{', '.join(missing_preferred_skills)}"
        )

    if missing_mandatory_skills:
        reasons.append(
            "Missing mandatory skills: "
            f"{', '.join(missing_mandatory_skills)}"
        )

    return reasons


def recommend_analysts(
    case: dict,
    complexity_label: str,
    top_n: int = 5,
) -> pd.DataFrame:
    analysts = load_analysts()

    required_skills = get_required_skills(case)
    mandatory_skills = get_mandatory_skills(case)

    results = []

    for _, analyst in analysts.iterrows():
        if analyst["availability_status"] == "Unavailable":
            continue

        analyst_skills = [
            skill.strip()
            for skill in analyst["skills"].split(",")
        ]

        skill_score, matched_skills = calculate_skill_score(
            required_skills,
            analyst_skills,
        )

        missing_mandatory_skills = [
            skill
            for skill in mandatory_skills
            if skill not in analyst_skills
        ]

        workload_score = calculate_workload_score(
            analyst["current_workload_pct"]
        )

        experience_score = calculate_experience_score(
            analyst["experience_years"],
            complexity_label,
        )

        availability_score = calculate_availability_score(
            analyst["availability_status"]
        )

        quality_score = calculate_quality_score(
            analyst["avg_completion_quality"]
        )

        raw_score = (
            skill_score
            + workload_score
            + experience_score
            + availability_score
            + quality_score
        )

        mandatory_skill_penalty = (
            35 * len(missing_mandatory_skills)
        )

        total_score = max(
            0,
            round(
                raw_score - mandatory_skill_penalty,
                1,
            ),
        )

        eligibility_status = (
            "Eligible"
            if not missing_mandatory_skills
            else "Fallback"
        )

        reasons = generate_reasons(
            analyst=analyst,
            required_skills=required_skills,
            matched_skills=matched_skills,
            missing_mandatory_skills=missing_mandatory_skills,
        )

        results.append({
            "analyst_id": analyst["analyst_id"],
            "analyst_name": analyst["analyst_name"],
            "seniority": analyst["seniority"],
            "team": analyst["team"],
            "skills": analyst["skills"],
            "current_workload_pct":
                analyst["current_workload_pct"],
            "availability_status":
                analyst["availability_status"],
            "suitability_score": total_score,
            "eligibility_status": eligibility_status,
            "required_skills":
                ", ".join(required_skills),
            "mandatory_skills":
                ", ".join(mandatory_skills),
            "matched_skills":
                ", ".join(matched_skills),
            "missing_mandatory_skills":
                ", ".join(missing_mandatory_skills),
            "skill_score": skill_score,
            "workload_score": workload_score,
            "experience_score": experience_score,
            "availability_score": availability_score,
            "quality_score": quality_score,
            "mandatory_skill_penalty":
                mandatory_skill_penalty,
            "reasons": reasons,
        })

    recommendations = pd.DataFrame(results)

    if recommendations.empty:
        raise ValueError(
            "No available analysts were found."
        )

    eligible_recommendations = recommendations[
        recommendations["eligibility_status"] == "Eligible"
    ].sort_values(
        by="suitability_score",
        ascending=False,
    )

    fallback_recommendations = recommendations[
        recommendations["eligibility_status"] == "Fallback"
    ].sort_values(
        by="suitability_score",
        ascending=False,
    )

    if not eligible_recommendations.empty:
        final_recommendations = pd.concat(
            [
                eligible_recommendations,
                fallback_recommendations,
            ],
            ignore_index=True,
        )
    else:
        print(
            "\nWARNING: No analyst matches all mandatory skills. "
            "Showing fallback candidates for manager review."
        )

        final_recommendations = (
            fallback_recommendations
            .reset_index(drop=True)
        )

    return final_recommendations.head(top_n)


if __name__ == "__main__":
    sample_case = {
        "fund_type": "UCITS",
        "num_sub_funds": 12,
        "num_delegates": 5,
        "aml_status": "Pending",
        "kyc_status": "Completed",
        "regulatory_review_required": 1,
    }

    top_recommendations = recommend_analysts(
        case=sample_case,
        complexity_label="High",
        top_n=5,
    )

    display_columns = [
        "analyst_name",
        "seniority",
        "team",
        "current_workload_pct",
        "availability_status",
        "suitability_score",
        "eligibility_status",
        "mandatory_skills",
        "matched_skills",
        "missing_mandatory_skills",
        "mandatory_skill_penalty",
    ]

    print("\nTOP ANALYST RECOMMENDATIONS")
    print(
        top_recommendations[
            display_columns
        ].to_string(index=False)
    )

    print("\nTOP RECOMMENDATION REASONS")

    for reason in top_recommendations.iloc[0]["reasons"]:
        print(f"- {reason}")