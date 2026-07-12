from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from ML.inference.predict_case import predict_case


app = FastAPI(
    title="Carne Compass API",
    description=(
        "AI-assisted fund onboarding complexity, "
        "effort and analyst recommendation API."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OnboardingCaseRequest(BaseModel):
    client_name: str = Field(
        min_length=2,
        max_length=100,
    )

    client_segment: Literal[
        "High Profile",
        "Institutional",
        "Small / Emerging",
    ]

    fund_type: Literal[
        "UCITS",
        "AIF",
        "Hedge Fund",
        "Private Equity",
        "Real Estate",
        "Money Market",
    ]

    domicile: Literal[
        "Ireland",
        "Luxembourg",
        "UK",
        "Cayman Islands",
        "Malta",
    ]

    aml_status: Literal[
        "Completed",
        "In Progress",
        "Pending",
        "Blocked",
    ]

    kyc_status: Literal[
        "Completed",
        "In Progress",
        "Pending",
        "Failed",
    ]

    risk_rating: Literal[
        "Low",
        "Medium",
        "High",
    ]

    client_priority: Literal[
        "Low",
        "Normal",
        "High",
        "Critical",
    ]

    latest_blocker_type: Literal[
        "None",
        "AML Delay",
        "KYC Issue",
        "Missing Documents",
        "Regulatory Review",
        "Analyst Unavailable",
        "Client Dependency",
    ] = "None"

    strategic_client: bool = False

    num_sub_funds: int = Field(ge=1, le=100)
    num_share_classes: int = Field(ge=1, le=200)
    num_jurisdictions: int = Field(ge=1, le=20)
    num_delegates: int = Field(ge=0, le=50)
    missing_documents: int = Field(ge=0, le=100)
    sla_days: int = Field(ge=1, le=365)
    regulatory_review_required: int = Field(ge=0, le=1)
    blocker_count: int = Field(ge=0, le=20)


@app.get("/")
def root() -> dict:
    return {
        "application": "Carne Compass",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "healthy",
        "model_loaded": True,
    }


@app.post("/api/v1/analyse")
def analyse_case(
    request: OnboardingCaseRequest,
) -> dict:
    try:
        case = request.model_dump()
        return predict_case(case)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {exc}",
        ) from exc