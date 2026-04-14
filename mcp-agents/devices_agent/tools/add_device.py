import uuid

from loguru import logger
from sqlalchemy import insert

from db.engine import SessionLocal
from db.models import Device
from schemas.device import AddDeviceRequest, AddDeviceResponse
from tools.sync_device import sync_device


async def add_device(request: AddDeviceRequest) -> AddDeviceResponse:
    device_id = uuid.uuid4()

    async with SessionLocal() as session:
        await session.execute(
            insert(Device).values(
                id=device_id,
                user_id=request.user_id,
                type_device=request.type_device,
                diagnosis_mock=request.diagnosis_mock,
            )
        )
        await session.commit()

    logger.info(f"Device registered: {device_id} type={request.type_device} user={request.user_id}")

    device = Device(
        id=device_id,
        user_id=request.user_id,
        type_device=request.type_device,
        diagnosis_mock=request.diagnosis_mock,
    )
    await sync_device(device)

    return AddDeviceResponse(success=True, device_id=str(device_id))
