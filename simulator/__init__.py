"""
simulator package — thin public wrapper around the generator implementation.
Provides a stable package name for the data-simulator component.
"""

# Re-export functions implemented in the `generator` package so callers can
# import from `simulator` while the implementation lives in `generator/`.
from simulator import generate_dataset, generate_dataframe
from simulator.cli import main as cli_main

__all__ = [
    "generate_dataset",
    "generate_dataframe",
    "cli_main",
]


