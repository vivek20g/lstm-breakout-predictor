"""
Moved spread_utils into generator package.
"""

import pandas as pd


def build_matrix_dict(df):
    col_keys = df.columns[1:]
    row_keys = df.iloc[:, 0]
    values = df.iloc[:, 1:]

    matrix_dict = {
        row_keys.iloc[i]: {
            col_keys[j]: values.iat[i, j]
            for j in range(len(col_keys))
        }
        for i in range(len(row_keys))
    }
    return matrix_dict


def get_buy_sell_spread(trade_direction, hour_of_day, order_month):
    xls = pd.read_excel("generator/data/Buy-Sell-Spread-Matrix.xlsx", sheet_name=None, engine='openpyxl')

    sell_low = build_matrix_dict(xls['sell_low'])
    sell_high = build_matrix_dict(xls['sell_high'])
    buy_low = build_matrix_dict(xls['buy_low'])
    buy_high = build_matrix_dict(xls['buy_high'])

    entry_spread = []
    exit_spread = []

    if trade_direction == "LONG":
        entry_spread = [buy_low[hour_of_day][order_month], buy_high[hour_of_day][order_month]]
        exit_spread = [sell_low[hour_of_day][order_month], sell_high[hour_of_day][order_month]]
    else:
        entry_spread = [sell_low[hour_of_day][order_month], sell_high[hour_of_day][order_month]]
        exit_spread = [buy_low[hour_of_day][order_month], buy_high[hour_of_day][order_month]]

    return entry_spread, exit_spread
