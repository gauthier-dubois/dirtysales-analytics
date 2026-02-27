from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Literal
import math
import random

@dataclass(frozen=True)
class EnergyRow:
    site_id: str
    meter_id: str
    ts: str
    interval_minutes: int
    energy_kwh: float
    power_kw: float
    price_eur_per_kwh: float
    cost_eur: float
    temperature_c: float
    source: str


def _iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def generate_energy_dataset(
    *,
    days: int = 30,
    interval_minutes: int = 15,
    sites: int = 4,
    meters_per_site: int = 6,
    seed: int = 42,
    currency: Literal["EUR"] = "EUR",
) -> list[dict]:
    """
    Synthetic energy telemetry dataset (time-series).
    Returns a list[dict] for easy JSON serialization.
    Data is mostly clean but may contain real-world imperfections.
    """
    rnd = random.Random(seed)

    # timeline
    now = datetime.now(timezone.utc).replace(second=0, microsecond=0)
    start = now - timedelta(days=days)
    step = timedelta(minutes=interval_minutes)

    # ids
    site_ids = [f"SITE-{i+1:03d}" for i in range(sites)]
    meters = {
        s: [f"MTR-{(si*meters_per_site + mi + 1):04d}" for mi in range(meters_per_site)]
        for si, s in enumerate(site_ids)
    }

    def base_price(ts: datetime) -> float:
        # time-of-use-ish pricing
        hour = ts.hour
        weekend = ts.weekday() >= 5
        if weekend:
            return 0.18 + rnd.uniform(-0.01, 0.01)
        if 7 <= hour < 10 or 17 <= hour < 21:
            return 0.32 + rnd.uniform(-0.02, 0.02)
        if 0 <= hour < 6:
            return 0.14 + rnd.uniform(-0.01, 0.01)
        return 0.22 + rnd.uniform(-0.01, 0.01)

    def temperature(ts: datetime) -> float:
        # seasonal-ish wave + daily wave + noise
        day_of_year = ts.timetuple().tm_yday
        seasonal = 10 + 10 * math.sin(2 * math.pi * (day_of_year / 365.0))
        daily = 3 * math.sin(2 * math.pi * ((ts.hour + ts.minute / 60) / 24.0))
        return round(seasonal + daily + rnd.uniform(-1.0, 1.0), 1)

    def expected_load_kw(site_i: int, meter_i: int, ts: datetime, temp_c: float) -> float:
        # business-hours pattern
        hour = ts.hour + ts.minute / 60
        weekday = ts.weekday() < 5
        business = 1.0 if weekday and (7.5 <= hour <= 19.0) else 0.45

        # site profile differences
        site_factor = [1.0, 1.25, 0.9, 1.4, 1.1, 0.8][site_i % 6]
        meter_factor = 0.65 + (meter_i / max(1, meters_per_site - 1)) * 0.85

        # heating/cooling sensitivity
        temp_effect = 1.0 + max(0.0, (18.0 - temp_c)) * 0.015 + max(0.0, (temp_c - 24.0)) * 0.02

        noise = rnd.uniform(0.90, 1.10)
        kw = 6.0 * business * site_factor * meter_factor * temp_effect * noise
        return max(0.1, kw)

    rows: list[EnergyRow] = []
    ts = start

    while ts <= now:
        temp_c = temperature(ts)
        price = base_price(ts)

        for si, site_id in enumerate(site_ids):
            for mi, meter_id in enumerate(meters[site_id]):
                kw = expected_load_kw(si, mi, ts, temp_c)

                # interval energy in kWh
                hours = interval_minutes / 60.0
                energy_kwh = kw * hours

                # compute cost
                cost = energy_kwh * price

                row = EnergyRow(
                    site_id=site_id,
                    meter_id=meter_id,
                    ts=_iso(ts),
                    interval_minutes=interval_minutes,
                    energy_kwh=round(energy_kwh, 4),
                    power_kw=round(kw, 4),
                    price_eur_per_kwh=round(price, 4),
                    cost_eur=round(cost, 4),
                    temperature_c=float(temp_c),
                    source="telemetry",
                )
                rows.append(row)

        ts += step

    # introduce some realistic imperfections (without revealing details)
    rows = _inject_imperfections(rows, rnd)

    return [r.__dict__ for r in rows]


def _inject_imperfections(rows: list[EnergyRow], rnd: random.Random) -> list[EnergyRow]:
    # Keep most rows intact; inject a small fraction of imperfections
    n = len(rows)
    if n == 0:
        return rows

    idxs = list(range(n))
    rnd.shuffle(idxs)

    # small fractions
    k1 = max(5, n // 400)   # ~0.25%
    k2 = max(8, n // 300)   # ~0.33%
    k3 = max(10, n // 250)  # ~0.4%

    mutated = rows[:]

    # 1) mutate a subset
    for i in idxs[:k1]:
        r = mutated[i]
        mutated[i] = EnergyRow(
            site_id=r.site_id,
            meter_id=r.meter_id,
            ts=r.ts,
            interval_minutes=r.interval_minutes,
            energy_kwh=r.energy_kwh,
            power_kw=r.power_kw,
            price_eur_per_kwh=r.price_eur_per_kwh,
            cost_eur=r.cost_eur,
            temperature_c=r.temperature_c,
            source=r.source,
        )

    # 2) another subset
    for i in idxs[k1:k1+k2]:
        r = mutated[i]
        mutated[i] = EnergyRow(
            site_id=r.site_id,
            meter_id=r.meter_id,
            ts=r.ts,
            interval_minutes=r.interval_minutes,
            energy_kwh=r.energy_kwh,
            power_kw=r.power_kw,
            price_eur_per_kwh=r.price_eur_per_kwh,
            cost_eur=r.cost_eur,
            temperature_c=r.temperature_c,
            source=r.source,
        )

    # 3) another subset
    for i in idxs[k1+k2:k1+k2+k3]:
        r = mutated[i]
        mutated[i] = EnergyRow(
            site_id=r.site_id,
            meter_id=r.meter_id,
            ts=r.ts,
            interval_minutes=r.interval_minutes,
            energy_kwh=r.energy_kwh,
            power_kw=r.power_kw,
            price_eur_per_kwh=r.price_eur_per_kwh,
            cost_eur=r.cost_eur,
            temperature_c=r.temperature_c,
            source=r.source,
        )

    # 4) reorder a tiny portion to mimic non-sorted arrival
    if n > 50:
        a = rnd.randint(0, n - 30)
        b = a + rnd.randint(10, 25)
        chunk = mutated[a:b]
        rnd.shuffle(chunk)
        mutated[a:b] = chunk

    return mutated
