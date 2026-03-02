# StockAgent Project - Input/Output Flow Explanation

## 📍 **WHERE INPUT IS GIVEN**

### 1. **Command Line Interface (CLI)**

**Location:** `src/stocksage/main.py`

**Input Method:**

```powershell
uv run python -m stocksage.main run
```

**What Gets Input:**

- **Hardcoded Inputs** (lines 41-46 in `main.py`):
  ```python
  inputs = {
      "market": "US",                    # Market to analyze
      "stock_universe": "S&P 500",       # Which stocks to analyze
      "current_year": "2025",            # Current year
      "analysis_date": "2025-11-09"       # Analysis date
  }
  ```

### 2. **Streamlit Web Interface**

**Location:** `src/stocksage/user_interface.py`

**Input Method:**

```powershell
uv run streamlit run src/stocksage/user_interface.py
```

**What Gets Input:**

- Interactive buttons in the web UI
- User clicks "Run Analysis" button
- Same inputs as CLI (hardcoded in the `run()` function)

### 3. **Environment Variables (.env file)**

**Location:** Root directory `.env` file (you need to create this)

**Required API Keys:**

```env
SERPER_API_KEY=your_key_here          # For news sentiment analysis
ALPHA_VANTAGE_KEY=your_key_here       # For financial data
OPENAI_API_KEY=your_key_here          # For AI agents
FIRECRAWL_API_KEY=your_key_here       # For web scraping
LANGSMITH_API_KEY=your_key_here       # For telemetry (optional)
```

---

## 🔄 **HOW THE SYSTEM PROCESSES INPUT**

### **Multi-Agent Workflow** (Hierarchical Process)

```
INPUT (market, stock_universe, date)
    ↓
┌─────────────────────────────────────┐
│  Portfolio Manager (Orchestrator)   │
└─────────────────────────────────────┘
    ↓
    ├─→ Fact Agent → Analyzes 500 stocks → Selects top 100
    ├─→ Sentiment Agent → Analyzes sentiment for 100 stocks
    ├─→ Analysis Agent → Integrates quantitative + sentiment
    ├─→ Recommendation Agent → Creates recommendations
    ├─→ Justification Agent → Validates selections
    ├─→ Optimization Agent → Refines selections
    ├─→ Synthesizer Agent → Selects top 5 stocks
    └─→ Thesis Agent → Generates investment theses
```

---

## 🔨 **WHERE AGENTS ARE BUILT IN THE CODE**

### **Agent Creation Functions** (Factory Pattern)

All agents are created using factory functions in `src/stocksage/agents.py`:

#### **1. Fact Agent** (Quantitative Financial Analyst)

**Location:** `src/stocksage/agents.py` lines **99-174**

**Function:** `create_fact_agent()`

- **Purpose:** Analyzes financial data to identify promising stocks (500 → 100)
- **Tools:** YFinanceTool, StockSymbolFetcherTool, AlphaVantageTool, Firecrawl tools
- **Key Configuration:**
  - Role: "Quantitative Financial Analyst" (from `agents.yaml` line 39)
  - Goal: "Deliver precise, data-driven financial analysis..."
  - Temperature: 0.3 (more deterministic)
  - Async Execution: True (can run tasks in parallel)
  - Allow Delegation: True (can delegate to other agents)

**Code Structure:**

```python
def create_fact_agent(agents_config, tools=[...], llm=FACT_AGENT_LLM, ...):
    fact_agent_config = agents_config.get("fact_agent", {})
    return Agent(
        role=fact_agent_config.get("role", "Fact Agent"),
        goal=fact_agent_config.get("goal", "Analyze financial data..."),
        tools=tools,  # Financial data tools
        allow_delegation=True,  # Can delegate work
        async_execution=True,   # Can run tasks in parallel
        ...
    )
```

#### **2. Sentiment Agent** (Market Perception Analyst)

**Location:** `src/stocksage/agents.py` lines **443-517**

**Function:** `create_sentiment_agent()`

- **Purpose:** Analyzes public sentiment and news for stock selection
- **Tools:** StockSymbolFetcherTool, SentimentAnalysisTool, Firecrawl tools
- **Key Configuration:**
  - Role: "Market Perception Analyst" (from `agents.yaml` line 89)
  - Goal: "Develop multi-dimensional sentiment profiles..."
  - Temperature: 0.5 (balanced creativity)
  - Special Instructions: Multi-dimensional sentiment analysis (financial media, consumer, leadership, digital, ESG)

**Code Structure:**

```python
def create_sentiment_agent(agents_config, tools=[...], ...):
    sentiment_agent_config = agents_config.get("sentiment_agent", {})
    return Agent(
        role=sentiment_agent_config.get("role", "Sentiment Analyst"),
        tools=[StockSymbolFetcherTool(), SentimentAnalysisTool(), ...],
        instructions="Perform comprehensive sentiment analysis...",
        ...
    )
```

#### **3. Analysis Agent** (Integrative Financial Strategist)

**Location:** `src/stocksage/agents.py` lines **29-95**

**Function:** `create_analysis_agent()`

- **Purpose:** Integrates quantitative and qualitative data for stock selection
- **Tools:** YFinanceTool, StockSymbolFetcherTool, SentimentAnalysisTool, AlphaVantageTool
- **Key Configuration:**
  - Role: "Integrative Financial Strategist" (from `agents.yaml` line 440)
  - Goal: "Develop unified analytical frameworks..."
  - Temperature: 0.4 (balanced)
  - Special Feature: Combines financial metrics with sentiment indicators

#### **4. Recommendation Agent** (Chief Investment Strategist)

**Location:** `src/stocksage/agents.py` lines **373-439**

**Function:** `create_recommendation_agent()`

- **Purpose:** Provides actionable investment recommendations
- **Tools:** YFinanceTool, SentimentAnalysisTool, StockSymbolFetcherTool, AlphaVantageTool
- **Key Configuration:**
  - Role: "Chief Investment Strategist" (from `agents.yaml` line 516)
  - Goal: "Transform comprehensive analyses into clear, actionable recommendations..."
  - Temperature: 0.5

#### **5. Justification Agent** (Investment Thesis Developer)

**Location:** `src/stocksage/agents.py` lines **178-240**

**Function:** `create_justification_agent()`

- **Purpose:** Provides reasoned justification for stock selections
- **Tools:** YFinanceTool, StockSymbolFetcherTool, SentimentAnalysisTool, AlphaVantageTool
- **Key Configuration:**
  - Role: "Investment Thesis Developer" (from `agents.yaml` line 142)
  - Goal: "Develop compelling, evidence-based investment rationales..."

#### **6. Optimization Agent** (Portfolio Construction Specialist)

**Location:** `src/stocksage/agents.py` lines **244-316**

**Function:** `create_optimization_agent()`

- **Purpose:** Optimizes stock selections based on risk-reward profiles
- **Tools:** YFinanceTool, SentimentAnalysisTool, StockSymbolFetcherTool, AlphaVantageTool
- **Key Configuration:**
  - Role: "Portfolio Construction Specialist" (from `agents.yaml` line 200)
  - Goal: "Design optimized investment portfolios..."
  - Temperature: 0.3 (more deterministic for optimization)

#### **7. Synthesizer Agent** (Chief Investment Strategist)

**Location:** `src/stocksage/agents.py` lines **521-596**

**Function:** `create_synthesizer_agent()`

- **Purpose:** Synthesizes diverse analyses to select top 5 stocks
- **Tools:** Empty list `[]` (works with outputs from other agents, not direct tools)
- **Key Configuration:**
  - Role: "Chief Investment Strategist" (from `agents.yaml` line 279)
  - Goal: "Identify the 5 most compelling investment opportunities..."
  - Special Note: Uses `tools=[]` because it synthesizes other agents' outputs

#### **8. Thesis Agent** (Investment Research Director)

**Location:** `src/stocksage/agents.py` lines **600-671**

**Function:** `create_thesis_agent()`

- **Purpose:** Creates institutional-quality investment theses
- **Tools:** YFinanceTool, SentimentAnalysisTool, StockSymbolFetcherTool, AlphaVantageTool
- **Key Configuration:**
  - Role: "Investment Research Director" (from `agents.yaml` line 353)
  - Goal: "Create institutional-quality investment theses..."
  - Temperature: 0.5

#### **9. Portfolio Manager** (Chief Investment Officer) - Orchestrator

**Location:** `src/stocksage/agents.py` lines **320-369**

**Function:** `create_portfolio_manger_agent()`

- **Purpose:** Oversees entire investment process and coordinates other agents
- **Tools:** None (orchestrates, doesn't directly analyze)
- **Key Configuration:**
  - Role: "Chief Investment Officer" (from `agents.yaml` line 2)
  - Goal: "Orchestrate the multi-stage investment analysis workflow..."
  - Allow Delegation: True (can delegate tasks to other agents)

---

### **Agent Instantiation in Crew** (Assembly Point)

All agents are instantiated and assembled in `src/stocksage/crew.py`:

#### **Agent Methods** (lines 66-181)

Each agent has a method decorated with `@agent` that calls the factory function:

```python
@agent
def fact_agent(self) -> Agent:
    """Creates the fact agent."""
    return create_fact_agent(self.agents_config)  # Line 90

@agent
def sentiment_agent(self) -> Agent:
    """Creates the sentiment agent."""
    return create_sentiment_agent(self.agents_config)  # Line 103

@agent
def analysis_agent(self) -> Agent:
    """Creates the analysis agent."""
    return create_analysis_agent(self.agents_config)  # Line 116

@agent
def recommendation_agent(self) -> Agent:
    """Creates the recommendation agent."""
    return create_recommendation_agent(self.agents_config)  # Line 181

@agent
def justification_agent(self) -> Agent:
    """Creates the justification agent."""
    return create_justification_agent(self.agents_config)  # Line 129

@agent
def optimization_agent(self) -> Agent:
    """Creates the optimization agent."""
    return create_optimization_agent(self.agents_config)  # Line 142

@agent
def synthesizer_agent(self) -> Agent:
    """Creates the synthesizer agent."""
    return create_synthesizer_agent(self.agents_config)  # Line 155

@agent
def thesis_agent(self) -> Agent:
    """Creates the thesis agent."""
    return create_thesis_agent(self.agents_config)  # Line 168

@agent
def portfolio_manager(self) -> Agent:
    """Creates the portfolio manager agent."""
    return create_portfolio_manger_agent(self.agents_config)  # Line 77
```

#### **Crew Assembly** (lines 447-484)

All agents are assembled into a Crew object in the `crew()` method:

```python
def crew(self) -> Crew:
    return Crew(
        agents=[
            self.fact_agent(),          # Line 449 - Analyzes 500 → 100 stocks
            self.sentiment_agent(),     # Line 450 - Analyzes sentiment
            self.analysis_agent(),      # Line 451 - Integrates data
            self.recommendation_agent(), # Line 452 - Creates recommendations
            self.justification_agent(), # Line 453 - Validates selections
            self.optimization_agent(),  # Line 454 - Refines selections
            self.synthesizer_agent(),   # Line 455 - Selects top 5
            self.thesis_agent(),        # Line 456 - Generates theses
        ],
        manager_agent=self.portfolio_manager(),  # Line 474 - Orchestrates
        process=Process.hierarchical,  # Hierarchical workflow
        ...
    )
```

---

### **Configuration Files**

Agent personalities and instructions come from:

- **`src/stocksage/config/agents.yaml`** - Contains role, goal, backstory, and detailed instructions for each agent
- **`src/stocksage/config.py`** - Contains LLM model assignments (e.g., `FACT_AGENT_LLM = "openai/gpt-4o"`)

---

### **Summary: Code Flow for Agent Creation**

```
1. Configuration Loaded
   └─→ agents.yaml read → agents_config dict

2. Factory Functions (agents.py)
   └─→ create_fact_agent(agents_config) → Returns Agent instance
   └─→ create_sentiment_agent(agents_config) → Returns Agent instance
   └─→ ... (8 total factory functions)

3. Crew Class Methods (crew.py)
   └─→ @agent def fact_agent() → calls create_fact_agent()
   └─→ @agent def sentiment_agent() → calls create_sentiment_agent()
   └─→ ... (8 agent methods)

4. Crew Assembly (crew.py line 447)
   └─→ Crew(agents=[self.fact_agent(), self.sentiment_agent(), ...])
   └─→ manager_agent=self.portfolio_manager()

5. Execution (main.py line 49)
   └─→ StockSage().crew().kickoff(inputs=inputs)
```

### **Task Execution Flow:**

1. **Stock Data Analysis** (`analyze_stock_data`)

   - Uses: `YFinanceTool`, `AlphaVantageTool`, `StockSymbolFetcherTool`
   - Input: Stock universe (S&P 500)
   - Output: Top 100 stocks based on financial metrics

2. **Sentiment Analysis** (`analyze_sentiment`)

   - Uses: `SentimentAnalysisTool`, `Firecrawl` tools
   - Input: 100 stocks from previous step
   - Output: Sentiment scores for each stock

3. **Integrated Analysis** (`perform_integrated_analysis`)

   - Combines financial + sentiment data
   - Output: Top 10 opportunities

4. **Final Selection** (`synthesize_final_selection`)

   - Input: Top 10 stocks
   - Output: Top 5 final recommendations

5. **Thesis Generation** (`generate_investment_thesis`)
   - Creates detailed investment theses
   - Output: Comprehensive analysis for each stock

---

## 📤 **WHERE OUTPUT COMES FROM**

### **Output Directory:** `outputs/`

All outputs are saved in the `outputs/` folder in the project root.

### **Output Files Generated:**

1. **`investment_thesis.json`**

   - **Location:** `outputs/investment_thesis.json`
   - **Content:** Full JSON with all investment theses
   - **Generated by:** `store_thesis_json` task
   - **Format:** Complete structured data

2. **`thesis_json.json`**

   - **Location:** `outputs/thesis_json.json`
   - **Content:** Simplified JSON with top 5 stocks
   - **Generated by:** `create_simplified_thesis_json` task
   - **Format:**
     ```json
     {
       "investments": [
         {
           "company_name": "Apple Inc.",
           "ticker": "AAPL",
           "thesis": "Investment thesis text..."
         }
       ]
     }
     ```

3. **`investment_report.md`**

   - **Location:** `outputs/investment_report.md`
   - **Content:** Executive summary and recommendations
   - **Generated by:** `manage_investment_process` task

4. **`termination_confirmation.md`**
   - **Location:** `outputs/termination_confirmation.md`
   - **Content:** Process completion confirmation
   - **Generated by:** `terminate_process` task

### **Additional Intermediate Outputs** (if configured):

- `stock_data_analysis.md` - Financial analysis results
- `sentiment_analysis.md` - Sentiment analysis results
- `integrated_analysis.md` - Combined analysis
- `final_selection_synthesis.md` - Final selection rationale

---

## 🔧 **HOW TO MODIFY INPUTS**

### **Option 1: Modify Code Directly**

Edit `src/stocksage/main.py` lines 41-46:

```python
inputs = {
    "market": "US",                    # Change to "EU", "ASIA", etc.
    "stock_universe": "NASDAQ-100",    # Change to "S&P 500", "DOW 30", etc.
    "current_year": str(datetime.now().year),
    "analysis_date": datetime.now().strftime("%Y-%m-%d"),
}
```

### **Option 2: Add Command-Line Arguments**

You could modify `main.py` to accept arguments:

```python
import sys

def run():
    market = sys.argv[2] if len(sys.argv) > 2 else "US"
    universe = sys.argv[3] if len(sys.argv) > 3 else "S&P 500"
    inputs = {
        "market": market,
        "stock_universe": universe,
        ...
    }
```

### **Option 3: Use Streamlit UI**

The UI could be enhanced to accept user inputs for market and stock universe.

---

## 📊 **PROJECT ARCHITECTURE SUMMARY**

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                           │
│  • Command: uv run python -m stocksage.main run         │
│  • API Keys: .env file                                  │
│  • Parameters: Hardcoded in main.py                     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│              CREWAI MULTI-AGENT SYSTEM                  │
│  • 8 Specialized Agents                                 │
│  • 13 Sequential Tasks                                   │
│  • Hierarchical Process (Portfolio Manager orchestrates)│
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    TOOLS USED                           │
│  • YFinanceTool - Stock data                            │
│  • AlphaVantageTool - Financial metrics                 │
│  • SentimentAnalysisTool - News sentiment               │
│  • StockSymbolFetcherTool - Get stock lists             │
│  • Firecrawl tools - Web scraping                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│                    OUTPUT FILES                        │
│  • outputs/investment_thesis.json                        │
│  • outputs/thesis_json.json                              │
│  • outputs/investment_report.md                          │
│  • outputs/termination_confirmation.md                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 **KEY TAKEAWAYS**

1. **Input Location:**

   - Hardcoded in `src/stocksage/main.py` (lines 41-46)
   - Can be run via CLI or Streamlit UI

2. **Processing:**

   - Multi-agent system processes inputs through 13 tasks
   - Agents use various tools to fetch and analyze data

3. **Output Location:**

   - All files saved to `outputs/` directory
   - Main outputs: JSON files with investment theses
   - Supporting outputs: Markdown reports

4. **To Change Inputs:**
   - Edit `main.py` directly, OR
   - Add command-line argument support, OR
   - Enhance Streamlit UI to accept user inputs
