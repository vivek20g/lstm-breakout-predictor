"""
generator package
Public API:
- generate_dataset(n_rows, out_path, seed=None) -> str (path to CSV)
- generate_dataframe(n_rows, seed=None) -> pandas.DataFrame

This package wraps code moved from the `multi-agent-feedback-loop` project
and provides a simple CLI for data generation.
"""

from .trade_generator import load_stock_data, generate_trade_metadata, apply_technical_indicators, re_assign_trade_directions
from .execution_price_simulator import generate_sample_execution_prices, calculate_trade_metrics

import pandas as pd
import os


def generate_dataframe(excel_path, sheet_name=None):
    """Load stock data, generate trade metadata, simulate execution and return DataFrame."""
    if sheet_name is None:
        sheet_name = 0
    df_stock = load_stock_data(excel_path, sheet_name)
    df_trades = generate_trade_metadata(df_stock)
    df_trades = apply_technical_indicators(df_trades)

    # simulate execution prices
    entry, exit = generate_sample_execution_prices(
        df_trades['EntryPrice'].tolist(),
        df_trades['ExitPrice'].tolist(),
        df_trades['MarketVolume'].tolist(),
        df_trades['volatility'].tolist() if 'volatility' in df_trades.columns else [0.0]*len(df_trades),
        df_trades['HourOfDay'].tolist(),
        df_trades['OrderMonth'].tolist(),
        df_trades['OrderQty'].tolist(),
        df_trades['TradeDirection'].tolist()
    )

    df_trades['AvgEntryExecutionPrice'] = entry
    df_trades['AvgExitExecutionPrice'] = exit

    df_trades = calculate_trade_metrics(df_trades)
    return df_trades


def generate_dataset(excel_path, out_path, sheet_name=None):
    """Create dataset and write to CSV at out_path. Returns out_path."""
    df = generate_dataframe(excel_path, sheet_name)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    df.to_csv(out_path, index=False)
    return out_path
