from typing import Optional
from datetime import datetime

from attrs import define

@define
class Report:
    cmd: str
    ret: str
    start: datetime
    end: datetime
    ex: Optional[Exception]