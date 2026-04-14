from pydantic import BaseModel, Field
from schemas.consilium import SpecialistFinding


class ConsiliumRequest(BaseModel):
    history_records: list[dict] = Field(
        default_factory=list,
        description="SOAP patient history records from client_history_agent.",
    )
    lab_records: list[dict] = Field(
        default_factory=list,
        description="Laboratory analysis records from labs_agent.",
    )


class ConsiliumResponse(BaseModel):
    findings: list[SpecialistFinding] = Field(
        description="Findings from all specialties that identified relevant issues."
    )
