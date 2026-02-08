from fastapi import APIRouter
from app.services.data_loader import load_raw_sales
from typing import Optional
from typing import List
import polars as pl
from app.services.cleaning import get_sales_clean
from app.services.analytics import compute_kpis, compute_data_quality, compute_timeseries
from app.models.dto import KpisDto, DataQualityColumnDto, SaledRowDto, TimeSeriesPointDto


router = APIRouter()

@router.get("/kpis", response_model=KpisDto)
def kpis():
    return compute_kpis()

@router.get("/data-quality", response_model=DataQualityColumnDto)
def data_quality():
    return compute_data_quality()

@router.get("/timeseries", response_model=List[TimeSeriesPointDto])
def timeseries(granularity: str = "day"):
    return compute_timeseries(granularity)

@router.get("/rows", response_model=List[SaledRowDto])
def rows(limit: int = 50, offset: int = 0, invalid_only: bool = False):
    df = get_sales_clean()

    if invalid_only:
        df = df.filter(pl.col("is_invalid") == True)

    page = df.slice(offset, limit)

    return page.select([
        "order_id","order_date","customer_id","country","category","product",
        "quantity","unit_price","discount_pct","shipping_cost","returned",
        "is_invalid","issues"
    ]).to_dicts()

@router.get("/rows/raw", response_model=List[SaledRowDto])
def raw_rows(limit: int = 20):
    df = load_raw_sales().head(limit)
    return df.to_dicts()
