import asyncio
import os
from datetime import datetime
from typing import Any

import aiohttp
import pandas as pd
from crewai.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field

from stocksage.utils import get_alpha_vantage_data, get_logger

load_dotenv()
logger = get_logger()


class AlphaVantageInput(BaseModel):
    """
    Input schema for Alpha Vantage API requests.

    This model defines the required and optional parameters for making
    requests to the Alpha Vantage financial data API.

    Attributes:
        ticker (str): Stock ticker symbol (required)
        function (str): Alpha Vantage API function to call (e.g., TIME_SERIES_DAILY)
        interval (str, optional): Time interval for intraday data. Defaults to "5min".
            Valid values: 1min, 5min, 15min, 30min, 60min
        output_format (str, optional): Desired output format. Defaults to "dict".
            Valid values: "dict" or "pandas"
    """

    ticker: str = Field(..., description="Stock ticker symbol")
    function: str = Field(
        ...,
        description=(
            "Alpha Vantage function to call (e.g., TIME_SERIES_DAILY, TIME_SERIES_INTRADAY)"
        ),
    )
    interval: str | None = Field(
        "5min",
        description="Data interval for intraday data (1min, 5min, 15min, 30min, 60min)",
    )
    output_format: str | None = Field("dict", description="Output format: 'dict' or 'pandas'")


class AlphaVantageTool(BaseTool):
    """
    Tool for retrieving financial data from Alpha Vantage API.

    This tool enables fetching various types of financial data including time series data,
    technical indicators, fundamental analysis, and more. The tool uses asynchronous
    API calls to efficiently retrieve data.

    Attributes:
        name (str): Name of the tool
        description (str): Detailed description of the tool's capabilities
        args_schema (Type[BaseModel]): Schema for validating input arguments
    """

    name: str = "Alpha Vantage Financial Data Tool"
    description: str = (
        "Retrieves detailed financial data from Alpha Vantage API. "
        "Can provide time series data (intraday, daily), fundamental analysis, "
        "technical indicators, and more.\n"
        "Available functions include TIME_SERIES_INTRADAY, TIME_SERIES_DAILY, OVERVIEW, "
        "GLOBAL_QUOTE, SMA, EMA, RSI, and more."
    )
    args_schema: type[BaseModel] = AlphaVantageInput

    # @traceable
    def _run(
        self,
        ticker: str,
        function: str,
        interval: str | None = "5min",
        output_format: str | None = "dict",
    ) -> dict[str, Any]:
        """
        Execute the Alpha Vantage API request and process the response.

        This method makes an asynchronous request to the Alpha Vantage API
        and formats the response according to the specified output format.

        Args:
            ticker (str): Stock ticker symbol to fetch data for
            function (str): Alpha Vantage API function to call
            interval (str, optional): Data interval for intraday data. Defaults to "5min".
            output_format (str, optional): Desired output format. Defaults to "dict".
                Options: "dict" or "pandas"

        Returns:
            Dict[str, Any] or pd.DataFrame:
                If output_format is "pandas", returns a pandas DataFrame with the data.
                Otherwise, returns a dictionary with:
                - ticker: The requested ticker symbol
                - function: The requested function
                - data: The actual data (as dictionary)
                - metadata: Additional information about the data (for DataFrame responses)
                - timestamp: ISO-formatted timestamp of when the data was retrieved

                In case of an error:
                - ticker: The requested ticker symbol
                - function: The requested function
                - error: Error message
                - message: Generic error description

        Raises:
            No exceptions are raised directly as they're caught and returned as error responses.
        """

        # Get API key from environment or use a default one
        api_key = os.getenv("ALPHA_VANTAGE_KEY", None)

        # Create async function to call get_alphavantage_data
        async def fetch_data() -> pd.DataFrame | dict:
            async with aiohttp.ClientSession() as session:
                return await get_alpha_vantage_data(ticker, api_key, session, function, interval)

        # Run async function in event loop
        try:
            # Always create a new event loop; get_event_loop() is deprecated in 3.10+
            try:
                loop = asyncio.get_running_loop()
                # We are inside a running loop — use run_coroutine_threadsafe
                import concurrent.futures

                future = concurrent.futures.Future()

                async def _run():
                    future.set_result(await fetch_data())

                asyncio.ensure_future(_run(), loop=loop)
                result = future.result(timeout=60)
            except RuntimeError:
                # No running loop — safe to create one
                loop = asyncio.new_event_loop()
                try:
                    result = loop.run_until_complete(fetch_data())
                finally:
                    loop.close()

            # Convert result based on output_format preference
            if isinstance(result, pd.DataFrame):
                if output_format.lower() == "pandas":
                    return result
                else:  # Convert to dict for JSON serialization
                    return {
                        "ticker": ticker,
                        "function": function,
                        "data": result.to_dict(orient="index"),
                        "metadata": {
                            "shape": result.shape,
                            "columns": list(result.columns),
                            "timestamp": datetime.now().isoformat(),
                        },
                    }
            else:
                return {
                    "ticker": ticker,
                    "function": function,
                    "data": result,
                    "timestamp": datetime.now().isoformat(),
                }

        except Exception as e:
            logger.error(f"Failed to fetch data from Alpha Vantage: {e}")
            return {
                "ticker": ticker,
                "function": function,
                "error": str(e),
                "message": "Failed to fetch data from Alpha Vantage API",
            }
