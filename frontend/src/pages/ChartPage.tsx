import { useEffect, useMemo, useState } from "react"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { fetchKpis, fetchTimeseries } from "@/lib/api"
import type { KpisDto, TimeSeriesPointDto } from "@/lib/types"
import { formatMoney } from "@/lib/format"
import { Line } from "@ant-design/charts"

export default function ChartPage() {
  const [kpis, setKpis] = useState<KpisDto | null>(null)
  const [series, setSeries] = useState<TimeSeriesPointDto[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setLoading(true)
    Promise.all([fetchKpis(), fetchTimeseries("day")])
      .then(([k, s]) => {
        setKpis(k)
        setSeries(s)
      })
      .finally(() => setLoading(false))
  }, [])

  const config = useMemo(
    () => ({
      data: series,
      xField: "date",
      yField: "revenue",
      height: 320,
      autoFit: true,
      smooth: true,
    }),
    [series]
  )

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="text-sm text-gray-500">Total revenue</CardHeader>
          <CardContent className="text-xl font-semibold">{kpis ? formatMoney(kpis.total_revenue) : "…"}</CardContent>
        </Card>

        <Card>
          <CardHeader className="text-sm text-gray-500">Orders</CardHeader>
          <CardContent className="text-xl font-semibold">{kpis ? kpis.order_count : "…"}</CardContent>
        </Card>

        <Card>
          <CardHeader className="text-sm text-gray-500">Avg order value</CardHeader>
          <CardContent className="text-xl font-semibold">{kpis ? formatMoney(kpis.avg_order_value) : "…"}</CardContent>
        </Card>

        <Card>
          <CardHeader className="text-sm text-gray-500">Invalid row rate</CardHeader>
          <CardContent className="text-xl font-semibold">{kpis ? `${Math.round(kpis.invalid_row_rate * 100)}%` : "…"}</CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="text-lg font-semibold">Revenue over time</div>
          <div className="text-sm text-gray-500">Basé sur /timeseries (DuckDB SQL)</div>
        </CardHeader>

        <CardContent>{loading ? <div className="text-sm text-gray-500">Loading…</div> : <Line {...config} />}</CardContent>
      </Card>
    </div>
  )
}