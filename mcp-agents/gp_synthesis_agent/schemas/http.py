from pydantic import BaseModel, Field


class SynthesisRequest(BaseModel):
    history_records: list[dict] = Field(
        default_factory=list,
        description="SOAP patient history records from client_history_agent.",
    )
    lab_records: list[dict] = Field(
        default_factory=list,
        description="Laboratory analysis records from labs_agent.",
    )
    device_records: list[dict] = Field(
        default_factory=list,
        description="Device and wearable data records from device_orchestrator_agent.",
    )
    complaint_records: list[dict] = Field(
        default_factory=list,
        description="Patient complaint records from complaint_manager_agent.",
    )
    consilium_findings: list[dict] = Field(
        default_factory=list,
        description="Specialist findings produced by the MDT consilium.",
    )
