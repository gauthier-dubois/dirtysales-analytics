from __future__ import annotations
import polars as pl
import threading
from app.services.data_loader import load_raw_sales

_country_map = {
    "belgium": "BE",
    "belgique": "BE",
    "be": "BE",
    "france": "FR",
    "fr": "FR",
    "netherlands": "NL",
    "nl": "NL",
    "de": "DE",
    "germany": "DE",
    "u.k.": "UK",
    "uk": "UK",
}

def _normalize_country(expr: pl.Expr) -> pl.Expr:
    return (
        expr.cast(pl.Utf8, strict=False)
        .str.strip_chars()
        .str.to_lowercase()
        .map_elements(lambda x: _country_map.get(x, x) if x is not None else None, return_dtype=pl.Utf8)
        .str.to_uppercase()
    )

def _parse_returned(expr: pl.Expr) -> pl.Expr:
    return (
        expr.cast(pl.Utf8, strict=False)
        .str.strip_chars()
        .str.to_lowercase()
        .map_elements(
            lambda x: (
                True if x in {"true", "1", "yes", "y"} else
                False if x in {"false", "0", "no", "n"} else
                None
            ) if x not in {None, ""} else None,
            return_dtype=pl.Boolean
        )
    )

_cached_clean: pl.DataFrame | None = None
_clean_lock = threading.Lock()

def get_sales_clean() -> pl.DataFrame:
    global _cached_clean


    if _cached_clean is not None:
        return _cached_clean

    with _clean_lock:
        if _cached_clean is not None:
            return _cached_clean

        raw = load_raw_sales()

        df = raw.with_columns(
            order_date_dt=pl.col("order_date").str.strptime(pl.Date, format="%Y-%m-%d", strict=False),
            quantity_num=pl.col("quantity").cast(pl.Float64, strict=False),
            unit_price_num=pl.col("unit_price").cast(pl.Float64, strict=False),
            discount_num=(
                pl.when(pl.col("discount_pct").cast(pl.Utf8, strict=False).str.contains("%"))
                  .then(
                      pl.col("discount_pct")
                        .cast(pl.Utf8, strict=False)
                        .str.replace("%", "")
                        .cast(pl.Float64, strict=False)
                  )
                  .otherwise(pl.col("discount_pct").cast(pl.Float64, strict=False))
            ),
            shipping_num=pl.col("shipping_cost").cast(pl.Float64, strict=False),
            returned_bool=_parse_returned(pl.col("returned")),
            country_norm=_normalize_country(pl.col("country")),
        )

        issues_expr = pl.concat_list(
            pl.when(pl.col("order_id").is_null() | (pl.col("order_id").cast(pl.Utf8, strict=False) == ""))
              .then(pl.lit("missing_order_id")).otherwise(pl.lit(None)),
            pl.when(pl.col("order_date").is_null() | (pl.col("order_date").cast(pl.Utf8, strict=False) == ""))
              .then(pl.lit("missing_order_date")).otherwise(pl.lit(None)),
            pl.when(pl.col("order_date_dt").is_null())
              .then(pl.lit("invalid_order_date")).otherwise(pl.lit(None)),
            pl.when(pl.col("customer_id").is_null() | (pl.col("customer_id").cast(pl.Utf8, strict=False) == ""))
              .then(pl.lit("missing_customer_id")).otherwise(pl.lit(None)),
            pl.when(pl.col("country").is_null() | (pl.col("country").cast(pl.Utf8, strict=False) == ""))
              .then(pl.lit("missing_country")).otherwise(pl.lit(None)),
            pl.when(pl.col("quantity_num").is_null()).then(pl.lit("missing_quantity")).otherwise(pl.lit(None)),
            pl.when(pl.col("quantity_num").is_not_null() & (pl.col("quantity_num") <= 0)).then(pl.lit("invalid_quantity")).otherwise(pl.lit(None)),
            pl.when(pl.col("unit_price_num").is_null()).then(pl.lit("missing_unit_price")).otherwise(pl.lit(None)),
            pl.when(pl.col("unit_price_num").is_not_null() & (pl.col("unit_price_num") <= 0)).then(pl.lit("invalid_unit_price")).otherwise(pl.lit(None)),
            pl.when(pl.col("discount_num").is_not_null() & ((pl.col("discount_num") < 0) | (pl.col("discount_num") > 100)))
              .then(pl.lit("invalid_discount_pct")).otherwise(pl.lit(None)),
            pl.when(pl.col("shipping_num").is_not_null() & (pl.col("shipping_num") < 0)).then(pl.lit("invalid_shipping_cost")).otherwise(pl.lit(None)),
            pl.when(pl.col("returned_bool").is_null()).then(pl.lit("invalid_returned")).otherwise(pl.lit(None)),
            pl.when(pl.col("category").is_null() | (pl.col("category").cast(pl.Utf8, strict=False) == ""))
              .then(pl.lit("missing_category")).otherwise(pl.lit(None)),
            pl.when(pl.col("product").is_null() | (pl.col("product").cast(pl.Utf8, strict=False) == ""))
              .then(pl.lit("missing_product")).otherwise(pl.lit(None)),
        ).list.drop_nulls()

        df = df.with_columns(
            issues=issues_expr,
            is_invalid=issues_expr.list.len() > 0,
        )

        _cached_clean = df
        return df
