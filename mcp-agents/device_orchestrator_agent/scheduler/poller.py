import asyncio
from datetime import date

from loguru import logger
from sqlalchemy import select

from config import settings
from db.engine import SessionLocal
from db.models import Device, DeviceLog
from sqlalchemy.sql import func
from tools.sync_device import sync_device


async def _devices_needing_sync() -> list[Device]:
    today = date.today()
    async with SessionLocal() as session:
        synced_today = (
            select(DeviceLog.device_id)
            .where(func.date(DeviceLog.date_log) == today)
            .scalar_subquery()
        )
        result = await session.execute(
            select(Device).where(Device.id.not_in(synced_today))
        )
        return list(result.scalars().all())


async def _run_poll_cycle() -> None:
    logger.info("Poller: checking devices for sync")
    try:
        devices = await _devices_needing_sync()
        if not devices:
            logger.info("Poller: all devices already synced today")
            return
        logger.info(f"Poller: syncing {len(devices)} device(s)")
        results = await asyncio.gather(*[sync_device(d) for d in devices], return_exceptions=True)
        succeeded = sum(1 for r in results if r is True)
        failed = len(results) - succeeded
        logger.info(f"Poller: cycle done — {succeeded} synced, {failed} failed")
    except Exception as exc:
        logger.error(f"Poller: cycle error: {exc}")


async def start_poller() -> None:
    logger.info(f"Poller: starting with interval={settings.poll_interval_seconds}s")
    while True:
        await _run_poll_cycle()
        await asyncio.sleep(settings.poll_interval_seconds)
