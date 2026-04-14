from loguru import logger
from sqlalchemy import select
from sqlalchemy.sql import func

from db.engine import SessionLocal
from db.models import Device, DeviceLog
from schemas.device import DeviceWithLastSync


async def get_patient_devices(user_id: str) -> list[DeviceWithLastSync]:
    async with SessionLocal() as session:
        latest_log = (
            select(DeviceLog.device_id, func.max(DeviceLog.date_log).label("last_sync"))
            .group_by(DeviceLog.device_id)
            .subquery()
        )

        result = await session.execute(
            select(Device, latest_log.c.last_sync)
            .outerjoin(latest_log, Device.id == latest_log.c.device_id)
            .where(Device.user_id == user_id)
            .order_by(Device.created_at)
        )

    rows = result.all()
    logger.info(f"Fetched {len(rows)} device(s) for user {user_id}")

    return [
        DeviceWithLastSync(
            id=str(device.id),
            user_id=device.user_id,
            type_device=device.type_device,
            diagnosis_mock=device.diagnosis_mock,
            created_at=device.created_at,
            last_sync=last_sync,
        )
        for device, last_sync in rows
    ]
