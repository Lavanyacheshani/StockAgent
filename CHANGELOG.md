# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Production hardening: LICENSE, CONTRIBUTING.md, SECURITY.md, CHANGELOG.md
- Pre-commit hooks configuration
- Type checking with pyright
- API health endpoint in FastAPI server
- Dockerfile OCI labels

### Changed
- Restricted CORS origins in server.py (configurable via environment variable)
- Added proper license and metadata fields to pyproject.toml

### Security
- Added rate limiting guidance
- Restricted bare `except` clauses

## [0.1.0] - 2025-03-13

### Added
- Initial release of StockAgent
- Hierarchical multi-agent system for US stock selection
- CrewAI-based agent orchestration with 9 specialized agents
- Alpha Vantage, Yahoo Finance, and Serper integrations
- VADER + TextBlob sentiment analysis
- LangSmith telemetry and tracing
- Streamlit UI for interactive analysis
- FastAPI backend with React frontend
- Docker and Docker Compose support
- GitHub Actions CI pipeline (lint, test, Docker build)
- MkDocs documentation site
- Comprehensive test suite with pytest

[Unreleased]: https://github.com/Lavanyacheshani/StockAgent/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Lavanyacheshani/StockAgent/releases/tag/v0.1.0
