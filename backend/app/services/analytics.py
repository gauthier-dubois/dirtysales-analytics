from __future__ import annotations
import duckdb
import polars as pl
import pandas as pd
from app.services.cleaning import get_sales_clean

def _con() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(database=":memory:")

def compute_kpis() -> dict:
    df: pl.DataFrame = get_sales_clean()

    with duckdb.connect(database=":memory:") as con:
        con.register("sales", df.to_pandas())

        res = con.execute("""
            WITH base AS (
            SELECT
                order_id,
                quantity_num,
                unit_price_num,
                COALESCE(discount_num, 0) AS discount_num,
                is_invalid
            FROM sales
            WHERE quantity_num IS NOT NULL
                AND unit_price_num IS NOT NULL
                AND quantity_num > 0
                AND unit_price_num > 0
            )
            SELECT
            COALESCE(SUM(quantity_num * unit_price_num * (1 - discount_num/100.0)), 0) AS total_revenue,
            COUNT(DISTINCT order_id) AS order_count,
            CASE WHEN COUNT(DISTINCT order_id) = 0 THEN 0
                ELSE COALESCE(SUM(quantity_num * unit_price_num * (1 - discount_num/100.0)), 0) / COUNT(DISTINCT order_id)
            END AS avg_order_value
            FROM base;
        """).fetchone()

    total_revenue, order_count, avg_order_value = res

    invalid_row_rate = float(df.select((pl.col("is_invalid").cast(pl.Float64)).mean()).item())
    return {
        "total_revenue": float(total_revenue),
        "order_count": int(order_count),
        "avg_order_value": float(avg_order_value),
        "invalid_row_rate": float(invalid_row_rate),
    }

def compute_data_quality() -> list[dict]:
    df = get_sales_clean()

    cols = ["order_id", "order_date", "customer_id", "country", "category", "product", "quantity", "unit_price", "discount_pct", "shipping_cost", "returned"]

    out = []
    n = df.height

    for c in cols:
        s = df.get_column(c)

        if s.dtype == pl.Utf8:
            missing = df.select((pl.col(c).is_null() | (pl.col(c) == "")).sum()).item()
        else:
            missing = df.select(pl.col(c).is_null().sum()).item()

        invalid = df.select(
            pl.col("issues").list.eval(pl.element().str.contains(c, literal=True)).list.any().sum()
        ).item()

        out.append({
            "column": c,
            "missing_rate": float(missing / n),
            "invalid_rate": float(invalid / n),
        })

    return out

def compute_timeseries(granularity: str = "day") -> list[dict]:
    df: pl.DataFrame = get_sales_clean()
    pdf = pd.DataFrame(df.to_dicts())

    if granularity not in {"day", "week", "month"}:
        granularity = "day"

    with duckdb.connect(database=":memory:") as con:
        con.register("sales", pdf)
        rows = con.execute(f"""
            WITH base AS (
                SELECT
                    order_date_dt,
                    quantity_num,
                    unit_price_num,
                    COALESCE(discount_num, 0) AS discount_num
                FROM sales
                WHERE order_date_dt IS NOT NULL
                  AND quantity_num IS NOT NULL AND quantity_num > 0
                  AND unit_price_num IS NOT NULL AND unit_price_num > 0
            )
            SELECT
                CAST(date_trunc('{granularity}', order_date_dt) AS VARCHAR) AS date,
                COALESCE(
                    SUM(quantity_num * unit_price_num * (1 - discount_num / 100.0)),
                    0
                ) AS revenue
            FROM base
            GROUP BY 1
            ORDER BY 1;
        """).fetchall()

    return [
        {"date": date, "revenue": float(revenue)}
        for date, revenue in rows
    ]