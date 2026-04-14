import uuid

from loguru import logger
from sqlalchemy import delete, select

from db.engine import SessionLocal
from db.models import Device, DeviceLog
from schemas.device import RemoveDeviceRequest, RemoveDeviceResponse


async def remove_device(request: RemoveDeviceRequest) -> RemoveDeviceResponse:
    try:
        device_id = uuid.UUID(request.device_id)
    except ValueError:
        return RemoveDeviceResponse(success=False, error=f"Invalid device_id: {request.device_id}")

    async with SessionLocal() as session:
        result = await session.execute(select(Device).where(Device.id == device_id))
        if result.scalar_one_or_none() is None:
            return RemoveDeviceResponse(success=False, error=f"Device {device_id} not found")

        await session.execute(delete(DeviceLog).where(DeviceLog.device_id == device_id))
        await session.execute(delete(Device).where(Device.id == device_id))
        await session.commit()

    logger.info(f"Device removed: {device_id}")
    return RemoveDeviceResponse(success=True)
