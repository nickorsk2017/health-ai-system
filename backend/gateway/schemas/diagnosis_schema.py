from pydantic import BaseModel


class GPConsultationSchema(BaseModel):
    diagnosis: str
    treatment: str
    prognosis: str
    summary: str
