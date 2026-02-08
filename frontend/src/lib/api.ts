import type { KpisDto, SalesRowDto, TimeSeriesPointDto } from "@/lib/types"

const BASE_URL = "http://127.0.0.1:8000"

async function getJson<T>(url: string): Promise<T> {
  const res = await fetch(url)
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return (await res.json()) as T
}

export function fetchRows(params: { limit?: number; offset?: number; invalid_only?: boolean }) {
  const u = new URL(`${BASE_URL}/rows`)
  if (params.limit != null) u.searchParams.set("limit", String(params.limit))
  if (params.offset != null) u.searchParams.set("offset", String(params.offset))
  if (params.invalid_only) u.searchParams.set("invalid_only", "true")
  return getJson<SalesRowDto[]>(u.toString())
}

export function fetchKpis() {
  return getJson<KpisDto>(`${BASE_URL}/kpis`)
}

export function fetchTimeseries(granularity: "day" | "week" | "month" = "day") {
  const u = new URL(`${BASE_URL}/timeseries`)
  u.searchParams.set("granularity", granularity)
  return getJson<TimeSeriesPointDto[]>(u.toString())
}