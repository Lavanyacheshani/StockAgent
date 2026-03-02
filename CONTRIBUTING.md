# Contributing to StockAgent

Thank you for your interest in contributing to StockAgent! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists in [GitHub Issues](https://github.com/Lavanyacheshani/StockAgent/issues).
2. If not, open a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the behavior
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

Open an issue tagged `enhancement` with:
- A clear description of the feature
- Why it would be useful
- Possible implementation approach

### Pull Requests

1. **Fork** the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Install** the development environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   uv sync --dev
   ```

3. **Make your changes** following the code style guidelines below.

4. **Add or update tests** for any new functionality:
   ```bash
   uv run pytest tests/ -v
   ```

5. **Run linting and formatting**:
   ```bash
   uv run ruff check src/ tests/
   uv run ruff format src/ tests/
   ```

6. **Commit** with a clear message following [Conventional Commits](https://www.conventionalcommits.org/):
   ```
   feat: add new sentiment data source
   fix: handle API timeout in alpha vantage tool
   docs: update installation instructions
   test: add tests for stock symbol fetcher
   ```

7. **Push** to your fork and open a Pull Request.

## Code Style

- We use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- Line length: 100 characters.
- Target Python version: 3.11.
- All public functions and classes must have docstrings.
- Use type hints for function parameters and return types.

## Testing

- Write tests for all new features and bug fixes.
- Use `pytest` markers for slow or integration tests:
  ```python
  @pytest.mark.integration
  def test_live_api_call():
      ...
  
  @pytest.mark.slow
  def test_full_pipeline():
      ...
  ```
- Integration tests requiring API keys are skipped in CI by default.

## Project Structure

```
src/stocksage/         # Main application code (import name: stocksage)
├── agents.py          # Agent definitions
├── config.py          # LLM and runtime configuration
├── crew.py            # CrewAI crew orchestration
├── main.py            # CLI entry points
├── tasks.py           # Task definitions
├── user_interface.py  # Streamlit UI
├── config/            # YAML agent/task configs
├── tools/             # Custom CrewAI tools
└── utils/             # Shared utilities
tests/                 # Test suite
server.py              # FastAPI backend
frontend/              # React frontend
```

## Questions?

Feel free to open a [Discussion](https://github.com/Lavanyacheshani/StockAgent/discussions) or reach out via Issues.
