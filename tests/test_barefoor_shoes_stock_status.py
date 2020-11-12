#!/usr/bin/env python

"""Tests for `barefoor_shoes_stock_status` package."""

import pytest

from typing import Set
from click.testing import CliRunner

from barefoor_shoes_stock_status import barefoor_shoes_stock_status
from barefoor_shoes_stock_status.parsers import VivoParser
from barefoor_shoes_stock_status import cli

VIVO_TEST_URL = "https://www.vivobarefoot.com/eu/mens/outdoor/magna-trail-leather-$4-wool-mens?colour=Obsidian"


def test_vivo_url_open():
    parser = VivoParser(VIVO_TEST_URL)
    site_html = parser.load_site()
    assert "Magna" in site_html


def test_get_sizes():
    parser = VivoParser(VIVO_TEST_URL)
    stock: Set[str] = parser.load_stock()
    eu42 = [size for size in stock if size.startswith("EU 42")]
    assert len(eu42) > 0


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "barefoor_shoes_stock_status.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
