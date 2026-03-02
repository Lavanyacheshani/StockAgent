"""Unit tests for SentimentAnalysisTool — uses mocking, no live network calls."""

from unittest.mock import patch

import pytest

from stocksage.tools.sentiment_analysis_tool import SentimentAnalysisTool


@pytest.fixture
def tool():
    return SentimentAnalysisTool(serper_api_key="fake-key-for-testing")


MOCK_NEWS = [
    {
        "title": "Apple reports record quarterly earnings",
        "snippet": "Apple Inc. posted revenue of $120B, beating analyst estimates.",
        "source": "Bloomberg",
        "link": "https://bloomberg.com/apple-earnings",
    },
    {
        "title": "AAPL stock rises on strong iPhone demand",
        "snippet": "iPhone 16 demand exceeds expectations in key markets.",
        "source": "Reuters",
        "link": "https://reuters.com/aapl",
    },
]


def test_run_returns_complete_sentiment_dict(tool):
    """SentimentAnalysisTool._run() should return a dict with all required keys."""
    with patch.object(tool, "fetch_stock_news", return_value=MOCK_NEWS):
        result = tool._run(ticker="AAPL", days=30)

    required_keys = {
        "ticker",
        "company_name",
        "overall_sentiment_score",
        "sentiment_label",
        "news_count",
        "social_media_mentions",
        "analyst_ratings",
        "news_items",
    }
    assert required_keys.issubset(result.keys()), f"Missing: {required_keys - result.keys()}"
    assert result["ticker"] == "AAPL"
    assert result["sentiment_label"] in {"Bullish", "Bearish", "Neutral"}
    assert -1.0 <= result["overall_sentiment_score"] <= 1.0
    assert result["news_count"] == len(MOCK_NEWS)


def test_run_with_no_news_returns_fallback(tool):
    """SentimentAnalysisTool._run() should handle empty news gracefully."""
    with patch.object(tool, "fetch_stock_news", return_value=[]):
        result = tool._run(ticker="AAPL", days=30)

    assert isinstance(result, dict)
    assert "overall_sentiment_score" in result
    assert result["news_count"] == 0


def test_run_with_custom_search_query(tool):
    """SentimentAnalysisTool._run() should accept a custom search query."""
    with patch.object(tool, "fetch_stock_news", return_value=MOCK_NEWS):
        result = tool._run(ticker="AAPL", days=7, search_query="CEO reputation")

    assert result["search_context"] == "CEO reputation"


def test_get_company_name_for_known_ticker(tool):
    """get_company_name_for_ticker() should return real names for known tickers."""
    assert tool.get_company_name_for_ticker("AAPL") == "Apple Inc."
    assert tool.get_company_name_for_ticker("MSFT") == "Microsoft Corporation"
    assert tool.get_company_name_for_ticker("NVDA") == "NVIDIA Corporation"


def test_get_company_name_fallback(tool):
    """get_company_name_for_ticker() should not crash on unknown tickers."""
    result = tool.get_company_name_for_ticker("ZZZZ")
    assert "ZZZZ" in result


def test_analyst_ratings_sum_to_25(tool):
    """Analyst ratings should always use 25 total analysts."""
    for score in [-0.9, -0.3, 0.0, 0.3, 0.9]:
        ratings = tool.get_deterministic_analyst_ratings(score)
        assert isinstance(ratings, dict)
        assert set(ratings.keys()) == {"buy", "hold", "sell"}
