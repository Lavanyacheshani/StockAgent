
# StockAgent

## Multi-Agent System for U.S. Stock Selection

**StockAgent** is a powerful AI-driven investment analysis platform designed to identify the top 5 U.S. stocks with the highest potential for market outperformance. Built on a robust hierarchical multi-agent architecture, it integrates real-time data analysis, sentiment interpretation, and financial modeling to deliver transparent and actionable investment recommendations.

---

## 🔍 Overview

StockAgent uses intelligent agents to perform:

- Fundamental and technical stock analysis
- Market sentiment extraction from news and social media
- Trend analysis and performance forecasting

It provides investors with holistic, explainable insights, supporting smarter and faster decision-making.

---

## 🚀 Features

- **Multi-Dimensional Stock Analysis**: Combines fundamentals, technicals, sentiment, and macroeconomic indicators.
- **Advanced Sentiment Analysis**: Real-time news and social sentiment processing.
- **Resilient Architecture**: Deterministic fallbacks ensure system stability during API failures.
- **LangSmith Telemetry Integration**: Full observability of agent behavior and decision rationale.
- **Customizable Analysis**: Adjust parameters to fit different investment goals.
- **Interactive Streamlit UI**: Simple interface for accessing stock recommendations.

---

## ⚙️ Prerequisites

- Python 3.10 or higher
- Docker (optional for deployment)

**API Keys Required**:

- Serper API (News sentiment)
- Alpha Vantage API (Financial data)
- LangChain API (Agent orchestration)
- OpenAI API

---

## 🛠️ Installation

### Local Setup

```bash
git clone https://github.com/yourusername/StockAgent.git
cd StockAgent
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
uv sync  # or pip install -r requirements.txt
```

### Docker Setup

```bash
docker build -t stockagent .
docker run -p 8501:8501 \
  -e SERPER_API_KEY=your_serper_api_key \
  -e ALPHAVANTAGE_API_KEY=your_alphavantage_api_key \
  -e LANGCHAIN_API_KEY=your_langchain_api_key \
  -e OPENAI_API_KEY=your_openai_api_key \
  -e LANGCHAIN_TRACING_V2=true \
  -e LANGCHAIN_ENDPOINT=https://api.smith.langchain.com \
  -e LANGSMITH_PROJECT=stock-agent \
  stockagent
```

---

## 📁 Configuration

Create a `.env` file in the project root:

```
SERPER_API_KEY=your_serper_api_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
OPENAI_API_KEY=your_openai_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=stock-agent
```

---

## 💻 Usage

### CLI Mode

```bash
python -m stockagent.main run        # Full pipeline
python -m stockagent.main train      # Train mode
python -m stockagent.main test       # Run test mode
python -m stockagent.main replay --run_id your_run_id
```

### Streamlit UI

```bash
streamlit run src/stockagent/user_interface.py
```

### Python API (CrewAI)

```python
from stockagent import StockAgent

inputs = {
    "market": "US",
    "stock_universe": "S&P 500",
    "current_year": "2025",
    "analysis_date": "2025-03-13"
}

agent = StockAgent()
results = agent.crew().kickoff(inputs=inputs)
print("Results saved to outputs directory.")
```

---

## 🧠 System Architecture

- **Data Collection Agents**: Fetch financials, news, and market data
- **Analysis Agents**: Interpret and evaluate data
- **Sentiment Agent**: Analyze public and media sentiment
- **Ranking Agent**: Score stocks and determine top performers
- **Thesis Agent**: Generate investment rationale for each stock

---

## 📤 Outputs

Located in the `outputs/` directory:

- JSON file with top 5 stock picks
- Sentiment scores and analysis
- Detailed investment theses
- Risk and volatility assessments
- Condensed summary reports

Example output:

```json
{
  "analysis_date": "2025-03-13",
  "investments": [
    {
      "ticker": "AAPL",
      "company_name": "Apple Inc.",
      "recommendation": "Buy",
      "target_price": "$210.45",
      "thesis": "Apple's strong ecosystem...",
      "sentiment_score": 0.78,
      "sentiment_label": "Bullish"
    }
  ]
}
```

---

## 🧪 Testing

```bash
pytest                  # Run all tests
pytest tests/test_sentiment_analysis_tool.py
pytest --cov=stockagent # Run with coverage report
```

---

## 🤝 Contributing

We welcome contributions! To contribute:

```bash
# Fork and clone
git checkout -b feature/your-feature
# Make changes and commit
git commit -m "Add your feature"
git push origin feature/your-feature
# Create a pull request
```

---

## 📄 License

StockAgent is open-source under the [MIT License](LICENSE).
