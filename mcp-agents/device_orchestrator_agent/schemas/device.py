import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

DeviceType = Literal["apple_health", "oura_ring"]


class AddDeviceRequest(BaseModel):
    user_id: str = Field(description="UUID of the patient who owns the device.")
    type_device: DeviceType = Field(description="Device type: 'oura_ring' or 'apple_health'.")
    diagnosis_mock: str | None = Field(
        default=None,
        description="Optional diagnosis for condition-specific data simulation (e.g. 'Pheochromocytoma').",
    )


class AddDeviceResponse(BaseModel):
    success: bool
    device_id: str


class RemoveDeviceRequest(BaseModel):
    device_id: str = Field(description="UUID of the device to remove.")


class RemoveDeviceResponse(BaseModel):
    success: bool
    error: str = ""


class DeviceWithLastSync(BaseModel):
    id: str
    user_id: str
    type_device: str
    diagnosis_mock: str | None
    created_at: datetime
    last_sync: datetime | None
