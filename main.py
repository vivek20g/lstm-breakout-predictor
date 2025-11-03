"""
main.py

Orchestrates the end-to-end pipeline for preparing features, building
and training an LSTM-based breakout predictor, and evaluating results.

Pipeline overview:
1. Read raw execution log data (Excel).
2. Enrich the DataFrame with engineered features:
   - add_price_dynamics: price deltas and volume-change features
   - add_technical_indicators: RSI, EMA, MACD, BB width, ATR, etc.
   - label_intraday_trade: creates `IntradayTradeIndicator` used as the
     3-class target (0: No Action, 1: Long Buy, 2: Short Sell)
3. Select and group columns into three feature sets used by the model:
   - price_features -> fed to `price_input` (sequence of price vectors)
   - indicator_features -> fed to `indicator_input` (sequence of indicators)
   - time_features -> fed to `time_input` (non-sequential per-row metadata)
4. `prepare_sequences` scales features (MinMaxScaler) and constructs
   overlapping sequences of length `sequence_length`. Scalers are persisted
   to `scalers/` for later inference.
5. Build a Keras model via `build_lstm_model` (returns an uncompiled model),
   train it (expects a compiled model), and evaluate using a simple holdout.

Notes & integration hints:
- Ensure that all columns referenced in `price_features`, `indicator_features`
  and `time_features` exist after feature engineering. If you compute new
  features (e.g. `volatility`), add them prior to calling
  `prepare_sequences`.
- `prepare_sequences` saves scalers; these must be used to transform raw
  inputs at inference to preserve the same scaling applied during training.
- The LSTM model expects inputs shaped as:
    Xp -> (batch_size, sequence_length, len(price_features))
    Xi -> (batch_size, sequence_length, len(indicator_features))
    Xt -> (batch_size, len(time_features))
  and labels as one-hot vectors with 3 classes.
- `build_lstm_model` returns an uncompiled model. Compile it (e.g.
  `model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])`)
  before calling `train_model` which calls `model.fit(...)`.

"""

import pandas as pd
from features import add_price_dynamics, add_technical_indicators, label_intraday_trade
from model import build_lstm_model, prepare_sequences, compute_class_weights, train_model, evaluate_model

def main():
    # Load raw execution log data. The sheet and engine used here match the
    # original data source; adjust path or sheet as needed.
    df = pd.read_excel("data/execution_log.xlsx", sheet_name="execution_log", engine="openpyxl")
    df = df.sort_values(by="ExecutionDate")

    # Feature engineering: these functions add derived columns in-place.
    # - add_price_dynamics: adds price-delta and volume-change features
    # - add_technical_indicators: computes indicators (RSI, EMA, MACD, ATR, ...)
    # - label_intraday_trade: creates the integer `IntradayTradeIndicator` column
    #   used as the 3-way classification target (0/1/2). Keep these calls in
    #   this order so rolling indicators align with the label calculation.
    df = add_price_dynamics(df)
    df = add_technical_indicators(df)
    df = label_intraday_trade(df)

    # Select the feature columns that will map to the three model inputs.
    # Make sure these column names exist in `df` after the feature engineering
    # step. If you add or rename engineered features, update these lists.
    price_features = ['Entry_vs_PrevClose', 'EntryPriceChange', 'volatility']
    indicator_features = ['EMA_10', 'EMA_20', 'MA50', 'BB_Width', 'RSI', 'Momentum', 'ATR']
    time_features = ['HourOfDay', 'OrderMonth', 'GoldenCrossover']

    # Sequence length chosen for overlapping windows. `prepare_sequences`
    # will scale the columns (MinMax) and persist scalers to `scalers/`.
    # The returned arrays have shapes compatible with the LSTM model inputs.
    sequence_length = 9
    Xp, Xi, Xt, y_train = prepare_sequences(df, price_features, indicator_features, time_features, sequence_length)

    # Compute class weights from the one-hot encoded labels to help with imbalance.
    class_weights = compute_class_weights(y_train)

    # Build the model that accepts three inputs.
    # NOTE: `build_lstm_model` returns an uncompiled model — compile it before training.
    model = build_lstm_model(sequence_length, len(price_features), len(indicator_features), len(time_features))

    # Important: compile the model prior to training. Example:
    # model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    # The current training utility (`train_model`) calls `model.fit(...)`, which
    # requires the model to be compiled first.

    history = train_model(model, Xp, Xi, Xt, y_train, class_weights)

    # Simple holdout evaluation: use the last `val_size` samples as a quick
    # validation set for visualization. For a proper evaluation use a
    # dedicated train/val/test split or cross-validation.
    val_size = int(len(y_train) * 0.3)
    evaluate_model(model, Xp[-val_size:], Xi[-val_size:], Xt[-val_size:], y_train[-val_size:])

    # Persist the trained model. You can load it later with
    # `tf.keras.models.load_model("model/daytrading_breakout_model.keras")` for inference.
    model.save("model/daytrading_breakout_model.keras")

if __name__ == "__main__":
    main()