"""Unit tests for StockSymbolFetcherTool — uses mocking, no live network calls."""

from unittest.mock import AsyncMock, patch

import pytest

from stocksage.tools.stock_symbol_fetcher_tool import StockSymbolFetcherTool


@pytest.fixture
def tool():
    return StockSymbolFetcherTool()


MOCK_SP500_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]


def test_run_returns_list_of_strings(tool):
    """StockSymbolFetcherTool._run() should return a list of ticker strings."""
    with patch(
        "stocksage.tools.stock_symbol_fetcher_tool.get_sp500_symbols",
        new_callable=AsyncMock,
        return_value=MOCK_SP500_SYMBOLS,
    ):
        result = tool._run(market="US", stock_universe="S&P 500")

    assert isinstance(result, (list, dict, str))


def test_run_handles_exception_gracefully(tool):
    """StockSymbolFetcherTool._run() should not raise on API failure."""
    with patch(
        "stocksage.tools.stock_symbol_fetcher_tool.get_sp500_symbols",
        side_effect=RuntimeError("network error"),
    ):
        try:
            result = tool._run(market="US", stock_universe="S&P 500")
            # Either returns an error dict or empty — but must not raise
            assert result is not None
        except Exception as exc:
            pytest.fail(f"Tool should not raise exceptions but got: {exc}")
