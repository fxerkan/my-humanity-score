"""Unit test conftest — no FastAPI app or database imports."""
# Unit tests are fully isolated: they only import pure Python modules
# (services/score_calculator.py, core/security.py) and do not need
# a running database or the full FastAPI application.
