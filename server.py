import json
import logging
import os
import subprocess

from fastapi import BackgroundTasks, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configuration
PROJECT_ROOT = os.getcwd()

# Cross-platform Python path detection
if os.name == "nt":
    PYTHON_PATH = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
else:
    PYTHON_PATH = os.path.join(PROJECT_ROOT, ".venv", "bin", "python")

# Fallback to sys.executable if venv python not found
if not os.path.exists(PYTHON_PATH):
    import sys
    PYTHON_PATH = sys.executable

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs")

# CORS: restrict to specific origins in production via ALLOWED_ORIGINS env var
# Example: ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("stockagent-api")

app = FastAPI(
    title="StockAgent Intelligence API",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Enable CORS for the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Shared State
execution_state = {
    "is_running": False,
    "last_run_id": None,
    "last_exit_code": None,
    "error": None
}

def run_analysis_task():
    global execution_state
    try:
        logger.info("Starting analysis execution...")
        execution_state["is_running"] = True
        execution_state["error"] = None

        # Execute the main run
        process = subprocess.run(
            [PYTHON_PATH, "-m", "stocksage.main", "run"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True
        )

        execution_state["last_exit_code"] = process.returncode

        if process.returncode != 0:
            execution_state["error"] = process.stderr
            logger.error(f"Analysis failed: {process.stderr}")
        else:
            logger.info("Analysis completed successfully. Syncing data...")
            # Sync and sanitize
            subprocess.run([PYTHON_PATH, "sync_data.py"], cwd=PROJECT_ROOT)
            subprocess.run([PYTHON_PATH, "sanitize_data.py"], cwd=PROJECT_ROOT)
            logger.info("Final data synchronization complete.")

    except Exception as e:
        execution_state["error"] = str(e)
        logger.error(f"Exception during analysis: {e}")
    finally:
        execution_state["is_running"] = False

@app.post("/api/run")
async def trigger_analysis(background_tasks: BackgroundTasks):
    if execution_state["is_running"]:
        return {"status": "error", "message": "Analysis already in progress"}

    background_tasks.add_task(run_analysis_task)
    return {"status": "started", "message": "Background analysis initiated"}

@app.get("/api/status")
async def get_status():
    return execution_state

@app.get("/api/results")
async def get_results():
    short_thesis_path = os.path.join(OUTPUT_DIR, "thesis_json.json")
    detailed_thesis_path = os.path.join(OUTPUT_DIR, "investment_thesis.json")

    results = {"investments": []}

    if os.path.exists(short_thesis_path):
        with open(short_thesis_path) as f:
            results = json.load(f)

    if os.path.exists(detailed_thesis_path):
        with open(detailed_thesis_path) as f:
            try:
                detailed_data = json.load(f)
                # Merge detailed data if found
                for stock in results.get("investments", []):
                    ticker = stock.get("ticker")
                    details = next(
                        (d for d in detailed_data
                         if d.get("ticker_symbol") == ticker),
                        None,
                    )
                    if details:
                        stock["details"] = details
            except (json.JSONDecodeError, TypeError, KeyError):
                logger.warning("Could not parse detailed thesis JSON")

    return results

@app.get("/api/health")
async def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {"status": "healthy", "version": "0.1.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
