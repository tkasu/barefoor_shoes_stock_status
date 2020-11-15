"""Main module."""
import os

from dotenv import load_dotenv
from barefoot_shoes_stock_status.parsers import VivoParser
from barefoot_shoes_stock_status.notifiers import DebugNotifier, TelegramNotifier
from barefoot_shoes_stock_status.subscriber import Subscriber


def main():
    load_dotenv()
    # notifier = DebugNotifier(on_poll=[], on_update=["@tomikasu"], on_error=["@tomikasu"])

    tele_token = os.getenv("TELE_TOKEN")
    tele_chat_id = os.getenv("TELE_CHAT_ID")
    notifier = TelegramNotifier(
        tele_token, tele_chat_id, on_update=["@tomikasu"], on_error=["@tomikasu"]
    )

    subs = Subscriber(
        url="https://www.vivobarefoot.com/eu/mens/outdoor/magna-trail-leather-$4-wool-mens?colour=Obsidian",
        parser_class=VivoParser,
        poll_frequency=1,
        notifier=notifier,
    )
    subs.subscribe()


if __name__ == "__main__":
    main()
