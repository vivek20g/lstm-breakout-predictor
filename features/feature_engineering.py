"""
features/feature_engineering.py

Provides feature construction utilities used to prepare the dataset for
sequence modeling. The functions in this module enrich a raw intraday
trading dataframe with price-delta features, technical indicators and
an integer label `IntradayTradeIndicator` suitable for 3-class
classification (No Action / Long Buy / Short Sell).

Relationships to other modules
- `train_model.prepare_sequences` expects three groups of features:
  * price_features: columns representing raw price-related series or
    engineered price dynamics (e.g. EntryPrice, Entry_vs_PrevClose, Open, Close)
  * indicator_features: technical indicators produced by this module
    (e.g. RSI, EMA_10, BB_Width, MACD, ATR, Momentum, GoldenCrossover)
  * time_features: non-sequential features (time-of-day, day-of-week,
    or other per-row metadata) that will be used as `time_input` in the model
- `label_intraday_trade` creates `IntradayTradeIndicator` with integer
  codes used by `train_model` and converted to one-hot by
  `tf.keras.utils.to_categorical(..., num_classes=3)`.

Label mapping (inferred):
- 0 -> No Action / non-profitable
- 1 -> Long Buy (profitable LONG)
- 2 -> Short Sell (profitable SHORT)

Notes
- After computing rolling indicators you should drop NaNs (this module
  returns a dataframe with rolling NaNs still present — caller should
  handle `dropna()` where appropriate).
- Scale numeric features (see `train_model.prepare_sequences`) before
  building sequences and training.
"""

import pandas as pd
import numpy as np
import ta

def add_price_dynamics(df):
    """Add simple price delta and volume-change features.

    Produces columns such as `Entry_vs_PrevClose`, `EntryPriceChange`,
    `ExitPriceChange` and `VolumeChange`. These augment the raw price
    series and are commonly included in `price_features` passed to
    `train_model.prepare_sequences`.
    """
    df['Entry_vs_PrevClose'] = df['EntryPrice'] - df['Close'].shift(1)
    df['Entry_vs_PrevOpen'] = df['EntryPrice'] - df['Open'].shift(1)
    df['EntryPriceChange'] = df['EntryPrice'].diff()
    df['ExitPriceChange'] = df['ExitPrice'].diff()
    df['VolumeChange'] = df['MarketVolume'].pct_change()
    return df

def add_technical_indicators(df):
    """Compute a set of technical indicators and derived features.

    Adds indicators like RSI, EMA_10, EMA_20, Bollinger band width,
    MACD (+signal), GoldenCrossover (binary), SMA50, Momentum, ATR, etc.

    These columns are intended to be used as `indicator_features`
    when preparing sequences for the LSTM model.
    """
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'], window=9).rsi()
    df['EMA_10'] = ta.trend.EMAIndicator(df['Close'], window=10).ema_indicator()
    df['EMA_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    bb = ta.volatility.BollingerBands(df['Close'], window=10, window_dev=2)
    df['BB_Width'] = bb.bollinger_wband()
    macd = ta.trend.MACD(df['Open'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['GoldenCrossover'] = np.where(df['MACD'] > df['MACD_Signal'], 1, 0)
    df['MA50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
    df['Momentum'] = ta.momentum.ROCIndicator(df['Open'], window=3).roc()
    df['TR'] = np.maximum(df['High'] - df['Low'], np.maximum(abs(df['High'] - df['Close'].shift(1)), abs(df['Low'] - df['Close'].shift(1))))
    df['ATR'] = df['TR'].rolling(5).mean()
    return df

def label_intraday_trade(df):
    """Create a 3-class label column `IntradayTradeIndicator`.

    Rules (as implemented):
    - If `ProfitLoss` > 0 and `TradeDirection` == "LONG" -> label 1
    - If `ProfitLoss` > 0 and `TradeDirection` != "LONG" -> label 2
    - Else -> label 0

    The returned dataframe has `IntradayTradeIndicator` and is
    cleaned with `dropna()` at the end of the function.
    """
    labels = []
    for i in range(len(df)):
        profit = df["ProfitLoss"].iloc[i]
        direction = df["TradeDirection"].iloc[i]
        if profit > 0:
            labels.append(1 if direction == "LONG" else 2)
        else:
            labels.append(0)
    df["IntradayTradeIndicator"] = labels
    return df.dropna()
