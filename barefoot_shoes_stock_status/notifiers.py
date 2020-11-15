import telegram
from typing import List
from barefoot_shoes_stock_status.models import StockStatus


class TelegramNotifier:
    on_poll: List[str]
    on_update: List[str]
    on_error: List[str]
    bot: telegram.Bot
    chat_id: str

    def __init__(
        self, token: str, chat_id: str, on_poll=None, on_update=None, on_error=None
    ):
        self.bot = telegram.Bot(token=token)
        self.chat_id = chat_id
        self.on_poll = on_poll if on_poll else []
        self.on_update = on_update if on_update else []
        self.on_error = on_error if on_error else []

    def notify_poll(self, url: str, items: StockStatus):
        to_update_str = " ".join(self.on_poll)
        table_html = "<pre>" + items.to_pandas().to_markdown(index="False") + "</pre>"
        message = f"{to_update_str}\nFetched new stock status for: {url}"
        self.bot.send_message(self.chat_id, message)
        self.bot.send_message(self.chat_id, table_html, parse_mode="html")

    def notify_update(self, url: str, old_items: StockStatus, new_items: StockStatus):
        to_update_str = " ".join(self.on_update)
        comparison_df = new_items.compare_to_older(old_items)
        message = f"{to_update_str}\nStock status update for: {url}"
        table_html = "<pre>" + comparison_df.to_markdown(index="False") + "</pre>"
        self.bot.send_message(self.chat_id, message)
        self.bot.send_message(self.chat_id, table_html, parse_mode="html")

    def notify_error(self, url: str, error):
        to_update_str = " ".join(self.on_error)
        message = f"{to_update_str}\nERROR when fetching: {url}\n{error}"
        self.bot.send_message(self.chat_id, message)


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
        print(
            to_update_str,
            "\n",
            f"Fetched new stock status for: {url}",
            "\n",
            items.to_pandas(),
        )

    def notify_update(self, url: str, old_items: StockStatus, new_items: StockStatus):
        to_update_str = " ".join(self.on_update)
        comparison_df = new_items.compare_to_older(old_items)
        print(
            to_update_str, "\n", f"Stock status update for: {url}", "\n", comparison_df
        )

    def notify_error(self, url: str, error):
        to_update_str = " ".join(self.on_error)
        print(to_update_str, "\n", f"ERROR when fetching: {url}", "\n", error)
