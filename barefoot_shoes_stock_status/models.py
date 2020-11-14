import re

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class StockItem:
    size_category: str
    size: int
    stock_status: str

    @classmethod
    def from_vivo_str(cls, s: str):
        groups = re.search(r"(\w{2}) (\d{2})\s?(\(.+\))?", s)
        if not groups:
            raise ValueError(f"Invalid Vivo Stock row parsed {s}")
        size_category = groups.group(1)
        size = int(groups.group(2))
        if stock_status := groups.group(3):
            stock_status = stock_status.replace("(", "").replace(")", "")
        else:
            stock_status = "In Stock"
        return cls(size_category=size_category, size=size, stock_status=stock_status)
