from pydantic import BaseModel, ConfigDict, Field


class SpecialistFinding(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    specialty: str = Field(description="Medical specialty that produced this finding.")
    risks: str
    treatment: str
    prognosis: str
    probable_diagnosis: str
