from typing import List
from barefoot_shoes_stock_status.models import StockStatus


class DebugNotifier:
    on_poll: List[str]
    on_update: List[str]
    on_error: List[str]

    def __init__(self, on_poll=None, on_update=None, on_error=None):
        self.on_poll = on_poll if on_poll else []
        self.on_update = on_update if on_update else []
        self.on_error = on_error if on_error else []

    def notify_poll(self, url: str, items: StockStatus):
        to_update_str = " ".join(self.on_poll)
        print(to_update_str, "\n", f"Fetched new stock status for: {url}", "\n", items.to_pandas())
