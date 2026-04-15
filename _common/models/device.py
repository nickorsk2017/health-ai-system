from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

DeviceType = Literal["apple_health", "oura_ring"]


class DeviceRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    type_device: str
    diagnosis_mock: str | None
    created_at: datetime
    last_sync: datetime | None
