#!/usr/bin/env python

"""Tests for `barefoot_shoes_stock_status` package."""

import pytest
import pandas as pd

from typing import Set
from click.testing import CliRunner

from barefoot_shoes_stock_status import barefoot_shoes_stock_status
from barefoot_shoes_stock_status.parsers import VivoParser
from barefoot_shoes_stock_status.models import StockItem, StockStatus
from barefoot_shoes_stock_status import cli

VIVO_TEST_URL = "https://www.vivobarefoot.com/eu/mens/outdoor/magna-trail-leather-$4-wool-mens?colour=Obsidian"


@pytest.mark.selenium
def test_vivo_url_open():
    parser = VivoParser(VIVO_TEST_URL)
    site_html = parser.load_site()
    assert "Magna" in site_html


@pytest.mark.selenium
def test_get_sizes():
    parser = VivoParser(VIVO_TEST_URL)
    stock = parser.load_stock()
    for size in stock:
        assert isinstance(size, StockItem)
    eu42 = [size for size in stock if size.size == 42]
    assert len(eu42) > 0


def test_vivo_str_to_stockitem_sold_out():
    test_str = "EU 42 (Sold Out)"
    stock_item = StockItem.from_vivo_str(test_str)
    assert isinstance(stock_item, StockItem)
    assert stock_item.size == 42
    assert stock_item.size_category == "EU"
    assert stock_item.stock_status == "Sold Out"


def test_vivo_str_to_stockitem_in_stock():
    test_str = "EU 44"
    stock_item = StockItem.from_vivo_str(test_str)
    assert isinstance(stock_item, StockItem)
    assert stock_item.size == 44
    assert stock_item.size_category == "EU"
    assert stock_item.stock_status == "In Stock"


def test_vivo_str_to_stockitem_few_in_stock():
    test_str = "EU 47 (Only 4 left in stock)"
    stock_item = StockItem.from_vivo_str(test_str)
    assert isinstance(stock_item, StockItem)
    assert stock_item.size == 47
    assert stock_item.size_category == "EU"
    assert stock_item.stock_status == "Only 4 left in stock"


def test_stock_status_to_pandas():
    item1 = StockItem("EU", 42, "In Stock")
    item2 = StockItem("EU", 44, "Only 4 left")
    status = StockStatus({item1, item2})
    stock = status.to_pandas()
    assert isinstance(stock, pd.DataFrame)
    cols = stock.columns
    assert "size_category" in cols
    assert "size" in cols
    assert "stock_status" in cols
    rows, _ = stock.shape
    assert rows == 2


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "barefoot_shoes_stock_status.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
