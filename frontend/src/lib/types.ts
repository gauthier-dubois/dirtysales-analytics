export type SalesRowDto = {
  order_id: string | null
  order_date: string | null
  customer_id: string | null
  country: string | null
  category: string | null
  product: string | null
  quantity: unknown
  unit_price: unknown
  discount_pct: unknown
  shipping_cost: unknown
  returned: unknown
  is_invalid: boolean
  issues: string[]
}

export type KpisDto = {
  total_revenue: number
  order_count: number
  avg_order_value: number
  invalid_row_rate: number
}

export type TimeSeriesPointDto = {
  date: string
  revenue: number
}