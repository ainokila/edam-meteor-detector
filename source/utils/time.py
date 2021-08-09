from typing import Optional
from datetime import date, datetime

def date_to_datetime(
    dt: date,
    hour: Optional[int] = 0,
    minute: Optional[int] = 0, 
    second: Optional[int] = 0) -> datetime:

    return datetime(dt.year, dt.month, dt.day, hour, minute, second)