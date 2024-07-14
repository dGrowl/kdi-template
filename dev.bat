@echo off
IF %1 == format (ruff format src tests)
IF %1 == init   (python -m venv venv && pip install -e .)
IF %1 == lint   (ruff check src tests)
IF %1 == test   (pytest -rP)
