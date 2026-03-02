"""Unit tests for YFinanceTool — uses mocking, no live network calls."""

from unittest.mock import patch

import pandas as pd
import pytest

from stocksage.tools.yahoo_finance_tool import YFinanceTool


@pytest.fixture
def tool():
    return YFinanceTool()


def test_run_returns_dict_with_all_fields(tool, mock_yfinance_data):
    """YFinanceTool._run() should return a dict with expected keys."""
    with patch(
        "stocksage.tools.yahoo_finance_tool.get_yfinance_data",
        return_value=mock_yfinance_data,
    ):
        result = tool._run(ticker="AAPL")

    assert isinstance(result, dict), "Result must be a dict"
    expected_keys = {
        "ticker",
        "company_name",
        "current_price",
        "market_cap",
        "pe_ratio",
        "pb_ratio",
        "revenue_growth",
        "profit_margin",
        "debt_to_equity",
        "current_ratio",
        "52w_change",
        "average_volume",
        "short_interest",
        "volatility",
    }
    assert expected_keys.issubset(result.keys()), f"Missing keys: {expected_keys - result.keys()}"
    assert result["ticker"] == "AAPL"
    assert result["company_name"] == "Apple Inc."


def test_run_returns_error_on_empty_data(tool):
    """YFinanceTool._run() should return an error dict when yfinance returns nothing."""
    with patch(
        "stocksage.tools.yahoo_finance_tool.get_yfinance_data",
        return_value=(pd.DataFrame(), {}),
    ):
        result = tool._run(ticker="INVALID999")

    assert "error" in result


def test_run_returns_error_on_exception(tool):
    """YFinanceTool._run() should catch exceptions and return an error dict."""
    with patch(
        "stocksage.tools.yahoo_finance_tool.get_yfinance_data",
        side_effect=RuntimeError("network failure"),
    ):
        result = tool._run(ticker="AAPL")

    assert "error" in result
