import uuid

from pydantic import BaseModel

from _common.models.device import DeviceRecord, DeviceType

# Backward-compatible alias
DeviceRecordSchema = DeviceRecord


class AddDeviceRequestSchema(BaseModel):
    user_id: uuid.UUID
    type_device: DeviceType
    diagnosis_mock: str | None = None


class AddDeviceResponseSchema(BaseModel):
    success: bool
    device_id: str


class RemoveDeviceResponseSchema(BaseModel):
    success: bool


__all__ = [
    "DeviceType",
    "DeviceRecord",
    "DeviceRecordSchema",
    "AddDeviceRequestSchema",
    "AddDeviceResponseSchema",
    "RemoveDeviceResponseSchema",
]
