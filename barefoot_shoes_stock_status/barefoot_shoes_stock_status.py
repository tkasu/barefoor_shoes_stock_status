"""Main module."""
from barefoot_shoes_stock_status.parsers import VivoParser
from barefoot_shoes_stock_status.notifiers import DebugNotifier
from barefoot_shoes_stock_status.subscriber import Subscriber


def main():
    subs = Subscriber(
        url="https://www.vivobarefoot.com/eu/mens/outdoor/magna-trail-leather-$4-wool-mens?colour=Obsidian",
        parser_class=VivoParser,
        poll_frequency=1,
        notify_with_class=DebugNotifier,
        notify_on_poll=[""],
        notify_on_update=["@tomikasu"],
        notify_on_error=["@tomikasu"],
    )

    subs.subscribe()


if __name__ == "__main__":
    main()
