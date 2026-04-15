from _common.models.device import DeviceRecord, DeviceType

from pydantic import BaseModel, Field

# Backward-compatible alias used by existing tool files
DeviceWithLastSync = DeviceRecord


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


__all__ = [
    "DeviceRecord",
    "DeviceType",
    "DeviceWithLastSync",
    "AddDeviceRequest",
    "AddDeviceResponse",
    "RemoveDeviceRequest",
    "RemoveDeviceResponse",
]
