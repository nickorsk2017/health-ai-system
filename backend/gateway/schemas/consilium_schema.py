from pydantic import BaseModel


class SpecialistFindingSchema(BaseModel):
    specialty: str
    risks: str
    treatment: str
    prognosis: str
    probable_diagnosis: str
