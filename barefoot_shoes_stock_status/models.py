import re
import pandas as pd
import pickle
import numpy as np
import os

from hashlib import md5
from dataclasses import dataclass
from typing import Set, Optional


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
    url: Optional[str] = None

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

    def persist_state(self):
        with open(self.filepath(self.url), "wb") as f:
            b = pickle.dumps(self)
            f.write(b)

    @classmethod
    def from_statefile(cls, url: str):
        filepath = cls.filepath(url)
        with open(filepath, "rb") as f:
            return pickle.loads(f.read())

    @staticmethod
    def filepath(url):
        if not url:
            raise ValueError("Can't get filename without 'url' set.")
        return os.path.join("state_files", md5(url.encode()).hexdigest())

    def __iter__(self):
        return iter(self.stock)

    def __eq__(self, other):
        if not isinstance(other, StockStatus):
            return False
        else:
            return self.stock == other.stock
