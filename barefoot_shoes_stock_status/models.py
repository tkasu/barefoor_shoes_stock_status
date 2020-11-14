import re
import pandas as pd

from dataclasses import dataclass
from typing import Set


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


@dataclass(frozen=True)
class StockStatus:
    stock: Set[StockItem]

    def to_pandas(self):
        df = pd.DataFrame([item for item in self.stock])
        df = df.sort_values(by="size")
        return df

    def __iter__(self):
        return iter(self.stock)
