from attrs import define
from typing import Optional
from datetime import datetime

@define
class Report:
    cmd: str
    ret: str
    start: datetime
    end: datetime
    ex: Optional[Exception]