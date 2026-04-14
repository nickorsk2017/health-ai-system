import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel

DeviceType = Literal["apple_health", "oura_ring"]


class AddDeviceRequestSchema(BaseModel):
    user_id: uuid.UUID
    type_device: DeviceType
    diagnosis_mock: str | None = None


class AddDeviceResponseSchema(BaseModel):
    success: bool
    device_id: str


class DeviceRecordSchema(BaseModel):
    id: str
    user_id: str
    type_device: str
    diagnosis_mock: str | None
    created_at: datetime
    last_sync: datetime | None


class RemoveDeviceResponseSchema(BaseModel):
    success: bool
