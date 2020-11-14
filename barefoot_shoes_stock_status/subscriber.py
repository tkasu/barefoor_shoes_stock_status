from time import sleep
from typing import Optional
from barefoot_shoes_stock_status.parsers import VivoParser
from barefoot_shoes_stock_status.notifiers import DebugNotifier
from barefoot_shoes_stock_status.models import StockStatus


class Subscriber:
    url: str
    parser: VivoParser
    poll_frequency_s: int
    notifier: DebugNotifier
    state: Optional[StockStatus]

    def __init__(
        self,
        url,
        parser_class,
        poll_frequency,
        notify_with_class,
        notify_on_poll,
        notify_on_update,
        notify_on_error,
    ):
        self.url = url
        parser = parser_class(url)
        self.parser = parser
        self.poll_frequency_s = poll_frequency * 60
        self.notifier = notify_with_class(
            on_poll=notify_on_poll, on_update=notify_on_update, on_error=notify_on_error
        )
        self.state = None  # TODO Add possibility to persist state to disk

    def poll(self):
        try:
            new_state = self.parser.load_stock()
            if not self.state == new_state:
                self.notifier.notify_update(self.url, self.state, new_state)
                self.state = new_state
            else:
                self.notifier.notify_poll(self.url, new_state)
        except Exception as e:
            self.notifier.notify_error(self.url, e)

    def subscribe(self):
        while True:
            self.poll()
            sleep(self.poll_frequency_s)
