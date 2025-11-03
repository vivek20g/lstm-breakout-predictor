"""Moved execution_price_simulator from multi-agent-feedback-loop.
"""

# ...existing code...
import random
import math
import numpy as np
import pandas as pd
from .. import spread_utils as _spread_utils

# adapt get_buy_sell_spread import
get_buy_sell_spread = _spread_utils.get_buy_sell_spread


def generate_random_number(volume, orderqty, volatility, lower, higher):
    # ...existing code...
    try:
        log_values = [math.log(volume), math.log(orderqty), math.log(volatility)]
        weights = [0.2, 0.35, 0.45]
        weighted_sum = sum(w * lv for w, lv in zip(weights, log_values))
        random.seed(weighted_sum)
        return round(random.uniform(lower, higher), 4)
    except ValueError as e:
        print(f"Error generating random number: {e}")
        raise


def generate_sample_execution_prices(open_prices, close_prices, volume, volatility, hour_of_day, order_month, orderqty, trade_direction):
    # ...existing code...
    AvgEntryExecutionPrice = [None] * len(open_prices)
    AvgExitExecutionPrice = [None] * len(close_prices)

    for i in range(len(open_prices)):
        vol = volatility[i]
        if pd.isna(vol):
            continue

        entry_spread, exit_spread = get_buy_sell_spread(trade_direction[i], hour_of_day[i], order_month[i])

        AvgEntryExecutionPrice[i] = round(
            open_prices[i] * generate_random_number(volume[i], orderqty[i], abs(vol / 100), entry_spread[0], entry_spread[1]), 2
        )
        AvgExitExecutionPrice[i] = round(
            close_prices[i] * generate_random_number(volume[i], orderqty[i], abs(vol / 100), exit_spread[0], exit_spread[1]), 2
        )

    return AvgEntryExecutionPrice, AvgExitExecutionPrice


def calculate_trade_metrics(df):
    # ...existing code...
    df['TotalEntryTradeValue'] = df['AvgEntryExecutionPrice'] * df['ExecutedQty']
    df['TotalExitTradeValue'] = df['AvgExitExecutionPrice'] * df['ExecutedQty']

    df['EntryBrokerage'] = df['TotalEntryTradeValue'] * 0.02
    df['ExitBrokerage'] = df['TotalExitTradeValue'] * 0.02

    df['NetEntryAmount'] = np.where(
        df['TradeDirection'] == "SHORT",
        df['TotalEntryTradeValue'] - df['EntryBrokerage'],
        df['TotalEntryTradeValue'] + df['EntryBrokerage']
    )

    df['NetExitAmount'] = np.where(
        df['TradeDirection'] == "LONG",
        df['TotalExitTradeValue'] + df['ExitBrokerage'],
        df['TotalExitTradeValue'] - df['ExitBrokerage']
    )

    df['TotalTradeSlippageCost'] = np.where(
        df['TradeDirection'] == "LONG",
        ((df['AvgEntryExecutionPrice'] - df['EntryPrice']) + (df['ExitPrice'] - df['AvgExitExecutionPrice'])) * df['OrderQty'],
        ((df['EntryPrice'] - df['AvgEntryExecutionPrice']) + (df['AvgExitExecutionPrice'] - df['ExitPrice'])) * df['OrderQty']
    )

    df['ProfitLoss'] = np.where(
        df['TradeDirection'] == "LONG",
        df['NetExitAmount'] - df['NetEntryAmount'],
        df['NetEntryAmount'] - df['NetExitAmount']
    )

    return df.round(2)
