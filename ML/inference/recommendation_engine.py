import pandas as pd


ANALYSTS_PATH = "data/Synthetic/analysts.csv"


REQUIRED_SKILLS_BY_CASE = {
    "UCITS": ["UCITS"],
    "AIF": ["AIF"],
    "Hedge Fund": ["Hedge Fund"],
    "Private Equity": ["Private Equity"],
    "Real Estate": ["Real Estate"],
    "Money Market": ["UCITS"],
}


SENIORITY_LEVELS = {
    "Analyst": 1,
    "Senior Analyst": 2,
    "Associate": 2,
    "Senior Associate": 3,
    "Assistant Manager": 4,
    "Manager": 5,
}


def load_analysts(
    path: str = ANALYSTS_PATH,
) -> pd.DataFrame:
    return pd.read_csv(path)


def unique_skills(skills: list[str]) -> list[str]:
    return list(dict.fromkeys(skills))


def get_required_skills(case: dict) -> list[str]:
    required_skills = []

    required_skills.extend(
        REQUIRED_SKILLS_BY_CASE.get(
            case["fund_type"],
            [],
        )
    )

    if case["aml_status"] in [
        "In Progress",
        "Pending",
        "Blocked",
    ]:
        required_skills.append("AML")

    if case["kyc_status"] in [
        "In Progress",
        "Pending",
        "Failed",
    ]:
        required_skills.append("KYC")

    if case["regulatory_review_required"] == 1:
        required_skills.append("Regulatory")

    if (
        case["num_sub_funds"] >= 10
        or case["num_delegates"] >= 5
    ):
        required_skills.append("Complex Structures")

    return unique_skills(required_skills)


def get_mandatory_skills(case: dict) -> list[str]:
    mandatory_skills = []

    if case["fund_type"] in [
        "UCITS",
        "AIF",
        "Hedge Fund",
        "Private Equity",
        "Real Estate",
    ]:
        mandatory_skills.append(case["fund_type"])

    if case["aml_status"] in [
        "Pending",
        "Blocked",
    ]:
        mandatory_skills.append("AML")

    if case["kyc_status"] in [
        "Pending",
        "Failed",
    ]:
        mandatory_skills.append("KYC")

    if case["regulatory_review_required"] == 1:
        mandatory_skills.append("Regulatory")

    if (
        case["num_sub_funds"] >= 15
        or case["num_delegates"] >= 7
    ):
        mandatory_skills.append(
            "Complex Structures"
        )

    return unique_skills(mandatory_skills)


def calculate_skill_score(
    required_skills: list[str],
    analyst_skills: list[str],
) -> tuple[float, list[str]]:
    if not required_skills:
        return 35.0, []

    matched_skills = [
        skill
        for skill in required_skills
        if skill in analyst_skills
    ]

    coverage = (
        len(matched_skills)
        / len(required_skills)
    )

    return (
        round(coverage * 35, 1),
        matched_skills,
    )


def calculate_workload_score(
    workload_pct: float,
) -> float:
    if workload_pct <= 50:
        return 25.0

    if workload_pct <= 65:
        return 22.0

    if workload_pct <= 75:
        return 17.0

    if workload_pct <= 85:
        return 10.0

    if workload_pct <= 92:
        return 4.0

    return 0.0


def calculate_experience_score(
    experience_years: float,
    complexity_label: str,
) -> float:
    target_years = {
        "Low": 3,
        "Medium": 6,
        "High": 10,
    }.get(
        complexity_label,
        6,
    )

    score = (
        experience_years
        / target_years
        * 15
    )

    return round(
        min(score, 15),
        1,
    )


def calculate_availability_score(
    status: str,
) -> float:
    if status == "Available":
        return 10.0

    if status == "Limited":
        return 4.0

    return 0.0


def calculate_quality_score(
    avg_quality: float,
) -> float:
    return round(
        min(avg_quality / 5 * 10, 10),
        1,
    )


def calculate_seniority_score(
    seniority: str,
    complexity_label: str,
) -> float:
    level = SENIORITY_LEVELS.get(
        seniority,
        1,
    )

    minimum_level = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
    }.get(
        complexity_label,
        2,
    )

    if level >= minimum_level:
        return 5.0

    gap = minimum_level - level

    return max(
        0.0,
        5.0 - gap * 2.5,
    )


def generate_reasons(
    analyst: pd.Series,
    matched_skills: list[str],
    missing_required_skills: list[str],
    missing_mandatory_skills: list[str],
) -> list[str]:
    reasons = []

    if matched_skills:
        reasons.append(
            "Matches required skills: "
            + ", ".join(matched_skills)
        )

    workload = analyst[
        "current_workload_pct"
    ]

    if workload <= 65:
        reasons.append(
            f"Healthy workload at {workload}%"
        )
    elif workload <= 85:
        reasons.append(
            f"Manageable workload at {workload}%"
        )
    else:
        reasons.append(
            f"High workload at {workload}%"
        )

    reasons.append(
        analyst["availability_status"]
        + " for allocation"
    )

    reasons.append(
        f"{analyst['experience_years']} "
        "years of experience"
    )

    reasons.append(
        "Quality score "
        f"{analyst['avg_completion_quality']}/5"
    )

    if missing_required_skills:
        reasons.append(
            "Missing preferred skills: "
            + ", ".join(
                missing_required_skills
            )
        )

    if missing_mandatory_skills:
        reasons.append(
            "Missing mandatory skills: "
            + ", ".join(
                missing_mandatory_skills
            )
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
        if (
            analyst["availability_status"]
            == "Unavailable"
        ):
            continue

        analyst_skills = [
            skill.strip()
            for skill in str(
                analyst["skills"]
            ).split(",")
            if skill.strip()
        ]

        (
            skill_score,
            matched_skills,
        ) = calculate_skill_score(
            required_skills,
            analyst_skills,
        )

        missing_required_skills = [
            skill
            for skill in required_skills
            if skill not in analyst_skills
        ]

        missing_mandatory_skills = [
            skill
            for skill in mandatory_skills
            if skill not in analyst_skills
        ]

        is_eligible = (
            len(missing_mandatory_skills)
            == 0
        )

        workload_score = (
            calculate_workload_score(
                analyst[
                    "current_workload_pct"
                ]
            )
        )

        experience_score = (
            calculate_experience_score(
                analyst["experience_years"],
                complexity_label,
            )
        )

        availability_score = (
            calculate_availability_score(
                analyst[
                    "availability_status"
                ]
            )
        )

        quality_score = (
            calculate_quality_score(
                analyst[
                    "avg_completion_quality"
                ]
            )
        )

        seniority_score = (
            calculate_seniority_score(
                analyst["seniority"],
                complexity_label,
            )
        )

        total_score = round(
            skill_score
            + workload_score
            + experience_score
            + availability_score
            + quality_score
            + seniority_score,
            1,
        )

        reasons = generate_reasons(
            analyst=analyst,
            matched_skills=matched_skills,
            missing_required_skills=(
                missing_required_skills
            ),
            missing_mandatory_skills=(
                missing_mandatory_skills
            ),
        )

        results.append({
            "analyst_id":
                analyst["analyst_id"],
            "analyst_name":
                analyst["analyst_name"],
            "seniority":
                analyst["seniority"],
            "team":
                analyst["team"],
            "skills":
                analyst["skills"],
            "current_workload_pct":
                analyst[
                    "current_workload_pct"
                ],
            "availability_status":
                analyst[
                    "availability_status"
                ],
            "suitability_score":
                total_score,
            "eligibility_status": (
                "Eligible"
                if is_eligible
                else "Fallback"
            ),
            "is_eligible":
                is_eligible,
            "required_skills":
                ", ".join(
                    required_skills
                ),
            "mandatory_skills":
                ", ".join(
                    mandatory_skills
                ),
            "matched_skills":
                ", ".join(
                    matched_skills
                ),
            "missing_required_skills":
                ", ".join(
                    missing_required_skills
                ),
            "missing_mandatory_skills":
                ", ".join(
                    missing_mandatory_skills
                ),
            "missing_mandatory_count":
                len(
                    missing_mandatory_skills
                ),
            "skill_score":
                skill_score,
            "workload_score":
                workload_score,
            "experience_score":
                experience_score,
            "availability_score":
                availability_score,
            "quality_score":
                quality_score,
            "seniority_score":
                seniority_score,
            "reasons":
                reasons,
        })

    recommendations = pd.DataFrame(
        results
    )

    if recommendations.empty:
        raise ValueError(
            "No available analysts found."
        )

    eligible = recommendations[
        recommendations[
            "eligibility_status"
        ] == "Eligible"
    ].sort_values(
        by=[
            "suitability_score",
            "current_workload_pct",
            "quality_score",
        ],
        ascending=[
            False,
            True,
            False,
        ],
    )

    fallback = recommendations[
        recommendations[
            "eligibility_status"
        ] == "Fallback"
    ].sort_values(
        by=[
            "missing_mandatory_count",
            "skill_score",
            "current_workload_pct",
            "experience_score",
            "quality_score",
        ],
        ascending=[
            True,
            False,
            True,
            False,
            False,
        ],
    )

    final_recommendations = pd.concat(
        [
            eligible,
            fallback,
        ],
        ignore_index=True,
    )

    return final_recommendations.head(
        top_n
    )


if __name__ == "__main__":
    sample_case = {
        "fund_type": "UCITS",
        "num_sub_funds": 12,
        "num_delegates": 5,
        "aml_status": "Pending",
        "kyc_status": "Completed",
        "regulatory_review_required": 1,
    }

    recommendations = recommend_analysts(
        case=sample_case,
        complexity_label="High",
        top_n=5,
    )

    print(
        recommendations[
            [
                "analyst_name",
                "suitability_score",
                "eligibility_status",
                "matched_skills",
                "missing_mandatory_skills",
                "current_workload_pct",
            ]
        ].to_string(index=False)
    )