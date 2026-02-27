from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class EnergyTelemetryDto(BaseModel):
    site_id: str = Field(..., min_length=1)
    meter_id: str = Field(..., min_length=1)

    ts: datetime  # Pydantic parse automatiquement l'ISO string

    interval_minutes: int = Field(..., gt=0)

    energy_kwh: float
    power_kw: float
    price_eur_per_kwh: float
    cost_eur: float

    temperature_c: float

    source: Literal["telemetry"]

    class Config:
        from_attributes = True