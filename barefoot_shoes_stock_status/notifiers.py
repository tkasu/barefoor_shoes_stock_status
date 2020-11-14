from typing import Optional, Set, List
from barefoot_shoes_stock_status.models import StockItem


class DebugNotifier:
    on_poll: Optional[List[str]]
    on_update: Optional[List[str]]
    on_error: Optional[List[str]]

    def __init__(self, on_poll, on_update, on_error):
        self.on_poll = on_poll
        self.on_update = on_update
        self.on_error = on_error

    def notify_poll(self, items: Set[StockItem]):
        to_update_str = " ".join(self.on_poll)
        print(to_update_str, items)
