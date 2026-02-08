import { useEffect, useMemo, useState } from "react"
import { Table, Tag, Switch } from "antd"
import type { ColumnsType } from "antd/es/table"
import { Card, CardHeader, CardContent } from "@/components/ui/card"
import { fetchRows } from "@/lib/api"
import type { SalesRowDto } from "@/lib/types"
import { asString } from "@/lib/format"

export default function TablePage() {
  const [rows, setRows] = useState<SalesRowDto[]>([])
  const [loading, setLoading] = useState(false)
  const [invalidOnly, setInvalidOnly] = useState(false)

  useEffect(() => {
    console.log("je suis la")
    setLoading(true)
    fetchRows({ limit: 300, offset: 0, invalid_only: invalidOnly })
      .then(setRows)
      .finally(() => setLoading(false))
  }, [invalidOnly])

  const columns: ColumnsType<SalesRowDto> = useMemo(
    () => [
      { title: "Order", dataIndex: "order_id", key: "order_id", render: (v) => asString(v) || <span className="text-gray-400">missing</span> },
      { title: "Date", dataIndex: "order_date", key: "order_date", render: (v) => asString(v) || <span className="text-gray-400">missing</span> },
      { title: "Country", dataIndex: "country", key: "country" },
      { title: "Category", dataIndex: "category", key: "category" },
      { title: "Product", dataIndex: "product", key: "product" },
      { title: "Qty", dataIndex: "quantity", key: "quantity", render: (v) => asString(v) },
      { title: "Price", dataIndex: "unit_price", key: "unit_price", render: (v) => asString(v) },
      { title: "Discount", dataIndex: "discount_pct", key: "discount_pct", render: (v) => asString(v) },
      {
        title: "Invalid",
        dataIndex: "is_invalid",
        key: "is_invalid",
        render: (v: boolean) => (v ? <Tag color="red">YES</Tag> : <Tag color="green">OK</Tag>),
        filters: [
          { text: "Invalid", value: true },
          { text: "OK", value: false },
        ],
        onFilter: (value, record) => record.is_invalid === value,
      },
      {
        title: "Issues",
        dataIndex: "issues",
        key: "issues",
        render: (issues: string[]) =>
          issues?.length ? (
            <div className="flex flex-wrap gap-1">
              {issues.slice(0, 3).map((i) => (
                <Tag key={i} color="volcano">
                  {i}
                </Tag>
              ))}
              {issues.length > 3 ? <Tag>+{issues.length - 3}</Tag> : null}
            </div>
          ) : null,
      },
    ],
    []
  )

  return (
    <Card>
      <CardHeader className="flex items-center justify-between ">
        <div>
          <div className="text-lg font-semibold">Rows</div>
          <div className="text-sm text-gray-500">Affichage du CSV brut + flags de qualité</div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-sm text-gray-600">Invalid only</span>
          <Switch checked={invalidOnly} onChange={setInvalidOnly} />
        </div>
      </CardHeader>

      <CardContent>
        <Table<SalesRowDto>
          rowKey={(r, idx) => `${r.order_id ?? "missing"}-${idx}`} // stable par page
          loading={loading}
          scroll={{x: 1100}}
          columns={columns}
          dataSource={rows}
          pagination={{ pageSize: 25 }}
        />
      </CardContent>
    </Card>
  )
}