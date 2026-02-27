export type EnergyTelemetryDto = {
    site_id : string
    meter_id: string
    ts: string
    interval_minutes: number   
    energy_kwh: number
    power_kw: number
    price_eur_per_kwh: number
    cost_eur: number
    temperature_c: number
    source: string
}