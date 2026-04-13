import uuid
from datetime import date, datetime

from pydantic import BaseModel


class CreatePatientSchema(BaseModel):
    full_name: str
    dob: date
    gender: str


class PatientSchema(BaseModel):
    id: uuid.UUID
    full_name: str
    dob: date
    gender: str
    created_at: datetime
