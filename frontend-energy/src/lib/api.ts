import type { EnergyTelemetryDto } from "./types";

const BASE_URL = "http://127.0.0.1:8000";

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return (await res.json()) as T;
}

export function fetchEnergyTelemetry(params?: {
  days?: number;
  intervalMinutes?: number;
  sites?: number;
  metersPerSite?: number;
  seed?: number;
}) {
  const u = new URL(`${BASE_URL}/energy/telemetry`);
  if (params?.days != null) u.searchParams.set("days", String(params.days));
  if (params?.intervalMinutes != null)
    u.searchParams.set("interval_minutes", String(params.intervalMinutes));
  if (params?.sites != null) u.searchParams.set("sites", String(params.sites));
  if (params?.intervalMinutes != null)
    u.searchParams.set("meters_per_site", String(params.intervalMinutes));
  if (params?.seed != null) u.searchParams.set("seed", String(params.seed));
  return getJson<EnergyTelemetryDto[]>(u.toString());
}
