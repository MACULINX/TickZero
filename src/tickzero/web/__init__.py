# src/web/__init__.py
"""Web interface and database modules."""

from .match_database import MatchDatabase
from .web_interface import run_web_interface

__all__ = ['MatchDatabase', 'run_web_interface']
