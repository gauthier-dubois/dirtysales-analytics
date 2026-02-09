from pydantic import BaseModel
from typing import Optional, Any

class KpisDto(BaseModel):
    total_revenue: float
    order_count: int
    avg_order_value: float
    invalid_row_rate: float

class DataQualityColumnDto(BaseModel):
    column: str
    missing_rate: float
    invalid_rate: float

class SaledRowDto(BaseModel):
    order_id: Optional[str]
    order_date: Optional[str]
    customer_id: Optional[str]
    country: Optional[str]
    category: Optional[str]
    product: Optional[str]
    quantity: Optional[Any]
    unit_price: Optional[Any]
    discount_pct: Optional[Any]
    shipping_cost: Optional[Any]
    returned: Optional[Any]
    is_invalid: bool
    issues: list[str]
    
class TimeSeriesPointDto(BaseModel):
    date: str
    revenue: float

