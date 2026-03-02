import glob
import json
import os
import uuid
import webbrowser

import streamlit as st

from stocksage.utils.telemetry_tracking import verify_langsmith_setup

# Initialize LangSmith tracking (best-effort; app works without it)
verify_langsmith_setup()

# Page configuration
st.set_page_config(
    page_title="StockSage Dashboard", layout="wide", initial_sidebar_state="expanded"
)

# ─── Session-state defaults ───────────────────────────────────────────────────
for _key, _default in {
    "operation_running": False,
    "operation_result": None,
    "run_id": None,
    "current_operation": None,
    "train_iterations": 3,
    "train_filename": "training_output",
    "replay_task_id": "",
}.items():
    if _key not in st.session_state:
        st.session_state[_key] = _default

# Main header
st.title("📈 StockSage Dashboard")
st.markdown("AI-powered investment analysis with multi-agent architecture")

# ─── Sidebar: env-var validation warning ─────────────────────────────────────
REQUIRED_KEYS = [
    "OPENAI_API_KEY",
    "LANGSMITH_API_KEY",
    "ALPHA_VANTAGE_KEY",
    "SERPER_API_KEY",
    "FIRECRAWL_API_KEY",
]
missing_keys = [k for k in REQUIRED_KEYS if not os.getenv(k)]
if missing_keys:
    st.sidebar.warning(
        "⚠️ Missing environment variables:\n\n"
        + "\n".join(f"- `{k}`" for k in missing_keys)
        + "\n\nCopy `.env.example` → `.env` and fill in your keys."
    )

# Main content area
col1, col2 = st.columns([1, 2])

with col1:
    st.header("Operations")

    run_col1, run_col2 = st.columns(2)

    with run_col1:
        if st.button("📊 Run Analysis", use_container_width=True, key="btn_run"):
            st.session_state["operation_running"] = True
            st.session_state["current_operation"] = "run"
            st.session_state["run_id"] = str(uuid.uuid4())[:8]
            st.rerun()

        if st.button("🧪 Run Tests", use_container_width=True, key="btn_test"):
            st.session_state["operation_running"] = True
            st.session_state["current_operation"] = "test"
            st.session_state["run_id"] = str(uuid.uuid4())[:8]
            st.rerun()

    with run_col2:
        if st.button("🔄 Train Models", use_container_width=True, key="btn_train"):
            st.session_state["operation_running"] = True
            st.session_state["current_operation"] = "train"
            st.session_state["run_id"] = str(uuid.uuid4())[:8]
            st.rerun()

        if st.button("⏮️ Replay Run", use_container_width=True, key="btn_replay"):
            st.session_state["operation_running"] = True
            st.session_state["current_operation"] = "replay"
            st.session_state["run_id"] = str(uuid.uuid4())[:8]
            st.rerun()

    st.markdown("---")

    # ── Analysis configuration ────────────────────────────────────────────────
    st.header("Configuration")
    symbols = st.text_input(
        "Stock Symbols",
        "AAPL,MSFT,GOOGL,AMZN",
        help="Enter ticker symbols to analyse (comma-separated)",
        key="cfg_symbols",
    )

    time_period = st.select_slider(
        "Analysis Time Period",
        options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        value="1y",
        key="cfg_period",
    )

    market = st.selectbox(
        "Market",
        options=["US", "Global"],
        index=0,
        key="cfg_market",
    )

    stock_universe = st.selectbox(
        "Stock Universe",
        options=["S&P 500", "NASDAQ-100", "Dow 30"],
        index=0,
        key="cfg_universe",
    )

    st.markdown("---")

    # ── Train-specific controls ───────────────────────────────────────────────
    with st.expander("⚙️ Train Settings"):
        st.session_state["train_iterations"] = st.number_input(
            "Training iterations", min_value=1, max_value=20, value=3, step=1
        )
        st.session_state["train_filename"] = st.text_input(
            "Output filename", value="training_output"
        )

    # ── Replay-specific controls ──────────────────────────────────────────────
    with st.expander("⚙️ Replay Settings"):
        st.session_state["replay_task_id"] = st.text_input(
            "Task ID to replay", value=st.session_state["replay_task_id"]
        )

    st.markdown("---")

    # ── Output file selection ─────────────────────────────────────────────────
    st.header("Results")

    output_dir = "./outputs"
    json_files = glob.glob(f"{output_dir}/*.json")

    if not json_files:
        st.warning("No analysis files found. Run an analysis to generate results.")
        output_files = []
        selected_file = None
    else:
        output_files = sorted(
            [(os.path.basename(f), os.path.getmtime(f)) for f in json_files],
            key=lambda x: x[1],
            reverse=True,
        )
        output_files = [f[0] for f in output_files]
        selected_file = st.selectbox("Select Output File:", options=output_files, index=0)

    # ── LangSmith integration ─────────────────────────────────────────────────
    st.markdown("---")
    st.header("LangSmith Integration")

    langsmith_project = os.environ.get("LANGSMITH_PROJECT", "stock-sage")

    if st.button("🔗 Open in LangSmith", help="View traces in LangSmith"):
        webbrowser.open(f"https://smith.langchain.com/projects/{langsmith_project}")

# ─── Results display area ─────────────────────────────────────────────────────
with col2:
    if st.session_state.get("operation_running"):
        operation = st.session_state.get("current_operation", "run")
        run_id = st.session_state.get("run_id", "unknown")

        st.header(f"Running {operation.title()} (ID: {run_id})")

        progress_bar = st.progress(0)
        status_text = st.empty()

        # ── Build inputs from UI config ───────────────────────────────────────
        from datetime import datetime

        run_inputs = {
            "market": market,
            "stock_universe": stock_universe,
            "symbols": [s.strip() for s in symbols.split(",") if s.strip()],
            "time_period": time_period,
            "current_year": str(datetime.now().year),
            "analysis_date": datetime.now().strftime("%Y-%m-%d"),
        }

        result = None
        try:
            if operation == "run":
                status_text.text("Starting analysis…")
                progress_bar.progress(10)

                # Import here to avoid loading the whole pipeline at page load
                import nest_asyncio

                from stocksage.crew import StockSage

                nest_asyncio.apply()
                progress_bar.progress(30)
                status_text.text("Processing market data…")

                result = StockSage().crew().kickoff(inputs=run_inputs)

                progress_bar.progress(100)
                status_text.text("Analysis complete!")

            elif operation == "train":
                iterations = st.session_state["train_iterations"]
                filename = st.session_state["train_filename"] or "training_output"

                status_text.text(f"Training for {iterations} iterations…")
                progress_bar.progress(20)

                import nest_asyncio

                from stocksage.crew import StockSage

                nest_asyncio.apply()

                StockSage().crew().train(
                    n_iterations=iterations,
                    filename=filename,
                    inputs=run_inputs,
                )
                progress_bar.progress(100)
                status_text.text("Training complete!")
                result = {"message": f"Training saved to {filename}"}

            elif operation == "replay":
                task_id = st.session_state.get("replay_task_id", "").strip()
                if not task_id:
                    st.error("Please enter a Task ID in Replay Settings before replaying.")
                    st.session_state["operation_running"] = False
                    st.stop()

                status_text.text(f"Replaying task {task_id}…")
                progress_bar.progress(30)

                from stocksage.crew import StockSage

                StockSage().crew().replay(task_id=task_id)
                progress_bar.progress(100)
                status_text.text("Replay complete!")
                result = {"task_id": task_id}

            elif operation == "test":
                status_text.text("Running test mode (first task only)…")
                progress_bar.progress(25)

                import nest_asyncio

                from stocksage.crew import StockSage

                nest_asyncio.apply()

                crew_instance = StockSage().crew()
                test_task = crew_instance.tasks[0]
                agent = crew_instance.agents[0]

                progress_bar.progress(60)
                status_text.text("Executing test task…")

                try:
                    task_result = agent.execute_task(test_task)
                    result_str = str(task_result)
                    os.makedirs("outputs", exist_ok=True)
                    result_path = os.path.join("outputs", "test_result.txt")
                    with open(result_path, "w") as f:
                        f.write(result_str)
                    result = {"success": True, "result_path": result_path}
                except Exception as task_error:
                    result = {"success": False, "error": str(task_error)}

                progress_bar.progress(100)
                status_text.text("Test complete!")

            st.session_state["operation_result"] = {
                "status": "success",
                "message": f"{operation.title()} completed successfully",
                "data": result,
                "run_id": run_id,
            }

        except Exception as e:
            st.session_state["operation_result"] = {
                "status": "error",
                "message": f"Error during {operation}: {str(e)}",
                "error": str(e),
            }
            progress_bar.progress(100)
            status_text.text(f"❌ Error: {str(e)}")

        finally:
            st.session_state["operation_running"] = False

        if st.button("Reset", key="btn_reset"):
            st.session_state["operation_result"] = None
            st.rerun()

    elif selected_file:
        st.header("Analysis Results")

        # Show last operation result banner
        result = st.session_state.get("operation_result")
        if result:
            if result["status"] == "success":
                st.success(result["message"])
                if "run_id" in result:
                    langsmith_project = os.environ.get("LANGSMITH_PROJECT", "stock-sage")
                    st.info(f"Run ID: {result['run_id']}")
                    st.markdown(
                        f"[View in LangSmith](https://smith.langchain.com/projects/"
                        f"{langsmith_project}/runs?query={result['run_id']})"
                    )
            else:
                st.error(result["message"])

        # ── Load and display the selected output file ─────────────────────────
        try:
            with open(f"{output_dir}/{selected_file}") as f:
                data = json.load(f)

            # Detect field names flexibly
            if "investments" in data:
                investments = data.get("investments", [])
                analysis_date = data.get("analysis_date", "Not specified")
            elif "recommendations" in data:
                investments = data.get("recommendations", [])
                analysis_date = data.get("date", "Not specified")
            else:
                investments = []
                for value in data.values():
                    if (
                        isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict)
                    ) and any(k in value[0] for k in ["ticker", "symbol", "company"]):
                        investments = value
                        break
                analysis_date = data.get("date", data.get("timestamp", "Not specified"))

            st.subheader(f"Analysis Date: {analysis_date}")

            if investments:
                table_data = []
                for inv in investments:
                    ticker = inv.get("ticker", inv.get("symbol", "Unknown"))
                    company = inv.get("company_name", inv.get("company", ticker))
                    recommendation = inv.get("recommendation", inv.get("action", "Hold"))
                    target_price = inv.get("target_price", inv.get("price_target", "N/A"))

                    thesis = inv.get(
                        "thesis", inv.get("investment_thesis", inv.get("rationale", ""))
                    )
                    thesis_short = (thesis[:97] + "…") if len(thesis) > 100 else thesis

                    table_data.append(
                        {
                            "Ticker": ticker,
                            "Company": company,
                            "Recommendation": recommendation,
                            "Target Price": target_price,
                            "Thesis": thesis_short,
                        }
                    )

                st.dataframe(table_data, use_container_width=True)

                if table_data:
                    selected_ticker = st.selectbox(
                        "Select company for detailed view:",
                        options=[item["Ticker"] for item in table_data],
                        key="detail_ticker",
                    )

                    selected_investment = next(
                        (
                            inv
                            for inv in investments
                            if inv.get("ticker", inv.get("symbol", "")) == selected_ticker
                        ),
                        None,
                    )

                    if selected_investment:
                        st.subheader(f"Details for {selected_ticker}")

                        thesis = selected_investment.get(
                            "thesis",
                            selected_investment.get(
                                "investment_thesis",
                                selected_investment.get("rationale", "No thesis provided"),
                            ),
                        )

                        st.markdown("#### Investment Thesis")
                        st.info(thesis)

                        if "pros" in selected_investment and isinstance(
                            selected_investment["pros"], list
                        ):
                            st.markdown("#### Pros")
                            for pro in selected_investment["pros"]:
                                st.markdown(f"- {pro}")

                        if "cons" in selected_investment and isinstance(
                            selected_investment["cons"], list
                        ):
                            st.markdown("#### Cons")
                            for con in selected_investment["cons"]:
                                st.markdown(f"- {con}")
            else:
                st.warning("No investment recommendations found in the selected file.")

        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        st.info("No analysis files available. Run an analysis to generate results.")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
langsmith_project = os.environ.get("LANGSMITH_PROJECT", "stock-sage")
langsmith_endpoint = os.environ.get("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")

st.markdown(f"**LangSmith Project:** {langsmith_project} | **Endpoint:** {langsmith_endpoint}")
st.caption("StockSage · Multi-Agent Investment Analysis")
