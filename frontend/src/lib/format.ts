export function formatMoney(v: number) {
  return new Intl.NumberFormat("fr-BE", { style: "currency", currency: "EUR" }).format(v)
}

export function asString(v: unknown) {
  if (v === null || v === undefined) return ""
  return String(v)
}