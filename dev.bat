@echo off
IF %1 == lint   (ruff check src)
IF %1 == format (ruff format src)
IF %1 == init   (python -m venv venv && pip install -e .)
