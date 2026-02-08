from pathlib import Path
import polars as pl 
import threading

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "dirty_sales.csv"

_cached_raw: pl.DataFrame | None = None
_raw_lock = threading.Lock()

def load_raw_sales() -> pl.DataFrame:
    global _cached_raw

    if _cached_raw is not None:
        return _cached_raw

    with _raw_lock:
        if _cached_raw is not None:
            return _cached_raw

        df = pl.read_csv(
            DATA_PATH,
            infer_schema_length=2000,
            ignore_errors=True,
            null_values=["", "null", "None", "NA"],
        )
        _cached_raw = df
        return df