import re
import pandas as pd
import numpy as np

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

    def compare_to_older(self, other):
        df = self.to_pandas()
        if not isinstance(other, StockStatus):
            comp_df = df.rename(
                {"stock_status": "stock_status_new"}, errors="raise", axis=1
            )
            comp_df["stock_status_old"] = np.nan
            return comp_df
        else:
            other_df = other.to_pandas()
            comp_df = df.merge(
                other_df,
                on=["size_category", "size"],
                how="outer",
                suffixes=("_new", "_old"),
            )
            return comp_df

    def __iter__(self):
        return iter(self.stock)

    def __eq__(self, other):
        if not isinstance(other, StockStatus):
            return False
        else:
            return self.stock == other.stock
