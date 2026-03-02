"""
Shared pytest fixtures and configuration for StockAgent tests.
"""

import os
from datetime import UTC

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "integration: marks tests that call live APIs")
    config.addinivalue_line("markers", "slow: marks tests that take a long time")


def is_key_set(key: str) -> bool:
    return bool(os.getenv(key))


# ── Skip decorators ───────────────────────────────────────────────────────────
skip_no_openai = pytest.mark.skipif(
    not is_key_set("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set — skipping live OpenAI test",
)

skip_no_alpha_vantage = pytest.mark.skipif(
    not is_key_set("ALPHA_VANTAGE_KEY"),
    reason="ALPHA_VANTAGE_KEY not set — skipping live Alpha Vantage test",
)

skip_no_serper = pytest.mark.skipif(
    not is_key_set("SERPER_API_KEY"),
    reason="SERPER_API_KEY not set — skipping live Serper test",
)

skip_no_langsmith = pytest.mark.skipif(
    not is_key_set("LANGSMITH_API_KEY"),
    reason="LANGSMITH_API_KEY not set — skipping live LangSmith test",
)


# ── Common fixtures ───────────────────────────────────────────────────────────
@pytest.fixture
def mock_yfinance_data():
    """Return a minimal yfinance info dict for unit tests."""
    from datetime import datetime

    import pandas as pd

    hist = pd.DataFrame(
        {
            "Open": [180.0],
            "High": [182.0],
            "Low": [179.5],
            "Close": [181.0],
            "Volume": [1_000_000],
        },
        index=pd.DatetimeIndex([datetime.now(UTC)]),
    )
    info = {
        "longName": "Apple Inc.",
        "currentPrice": 181.0,
        "marketCap": 2_800_000_000_000,
        "trailingPE": 28.5,
        "priceToBook": 45.0,
        "revenueGrowth": 0.08,
        "profitMargins": 0.26,
        "debtToEquity": 150.0,
        "currentRatio": 1.15,
        "52WeekChange": 0.23,
        "averageVolume": 55_000_000,
        "shortPercentOfFloat": 0.007,
        "beta": 1.25,
    }
    return hist, info


@pytest.fixture
def mock_alpha_vantage_response():
    """Return a minimal Alpha Vantage OVERVIEW response for unit tests."""
    return {
        "Symbol": "AAPL",
        "Name": "Apple Inc",
        "Description": "Apple Inc. designs, manufactures, and markets smartphones.",
        "MarketCapitalization": "2800000000000",
        "PERatio": "28.5",
        "EPS": "6.35",
        "52WeekHigh": "198.23",
        "52WeekLow": "164.08",
    }
