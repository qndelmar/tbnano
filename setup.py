"""Compatibility shim so `pip install -e .` works on old pip (<21.3)
without PEP 660 support. All metadata lives in pyproject.toml."""

from setuptools import setup

setup()
