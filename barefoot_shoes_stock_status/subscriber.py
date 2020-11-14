from typing import Optional, Set
from barefoot_shoes_stock_status.parsers import VivoParser
from barefoot_shoes_stock_status.notifiers import DebugNotifier
from barefoot_shoes_stock_status.models import StockItem


class Subscriber:
    url: str
    parser: VivoParser
    poll_frequency_s: int
    notifier: DebugNotifier
    state: Optional[Set[StockItem]]

    def __init__(self, url, parser_class, poll_frequency, notify_with_class, notify_on_poll, notify_on_update, notify_on_error):
        self.site = url
        parser = parser_class(url)
        self.parser = parser
        self.poll_frequency_s = poll_frequency * 60
        self.notifier = notify_with_class(on_poll=notify_on_poll, on_update=notify_on_update, on_error=notify_on_error)

    def poll(self):
        new_state = self.parser.load_stock()
        self.notifier.notify_poll(new_state)


