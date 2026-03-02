"""Unit tests for AlphaVantageTool — uses mocking, no live network calls."""

from unittest.mock import AsyncMock, patch

import pandas as pd
import pytest

from stocksage.tools.alpha_vantage_tool import AlphaVantageTool


@pytest.fixture
def tool():
    return AlphaVantageTool()


def test_run_overview_returns_dict(tool, mock_alpha_vantage_response):
    """AlphaVantageTool._run() for OVERVIEW should return a dict."""
    with patch(
        "stocksage.tools.alpha_vantage_tool.get_alpha_vantage_data",
        new_callable=AsyncMock,
        return_value=mock_alpha_vantage_response,
    ):
        result = tool._run(ticker="AAPL", function="OVERVIEW")

    assert isinstance(result, dict)
    assert result.get("function") == "OVERVIEW" or "Symbol" in result


def test_run_time_series_returns_dict(tool):
    """AlphaVantageTool._run() for TIME_SERIES_DAILY should return a dict."""
    mock_df = pd.DataFrame(
        {"Open": [180.0], "High": [182.0], "Low": [179.0], "Close": [181.0], "Volume": [1e6]}
    )
    with patch(
        "stocksage.tools.alpha_vantage_tool.get_alpha_vantage_data",
        new_callable=AsyncMock,
        return_value=mock_df,
    ):
        result = tool._run(ticker="AAPL", function="TIME_SERIES_DAILY")

    assert isinstance(result, dict)
    assert "ticker" in result


def test_run_returns_error_dict_on_exception(tool):
    """AlphaVantageTool._run() should return an error dict on failure."""
    with patch(
        "stocksage.tools.alpha_vantage_tool.get_alpha_vantage_data",
        side_effect=RuntimeError("API error"),
    ):
        result = tool._run(ticker="AAPL", function="TIME_SERIES_DAILY")

    assert isinstance(result, dict)
    assert "error" in result
