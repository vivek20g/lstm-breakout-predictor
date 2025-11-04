"""
simulator package — thin public wrapper around `generator`.
Provides a stable package name for the data-simulator component.
"""

from simulator import generate_dataset, generate_dataframe
from simulator.cli import main as cli_main

__all__ = [
    "generate_dataset",
    "generate_dataframe",
    "cli_main",
]
