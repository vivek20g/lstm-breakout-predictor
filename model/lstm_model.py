"""
model/lstm_model.py

Defines the LSTM-based classification model and documents how its
inputs correspond to features produced by `features/feature_engineering.py`
and consumed by `model/train_model.py`.

Input mapping to pipeline
- price_input (shape: (sequence_length, price_dim))
  -> constructed from columns passed as `price_features` to
     `train_model.prepare_sequences`. These typically include raw price
     columns and engineered price dynamics (e.g. EntryPrice, Open, Close,
     Entry_vs_PrevClose, EntryPriceChange).
- indicator_input (shape: (sequence_length, indicator_dim))
  -> built from `indicator_features` produced by
     `features.add_technical_indicators` (e.g. RSI, EMA_10, BB_Width, MACD,
     GoldenCrossover, ATR, Momentum, MA50).
- time_input (shape: (time_dim,))
  -> non-sequential per-row features passed as `time_features` to
     `prepare_sequences` (e.g. time-of-day encodings, day-of-week,
     or other metadata). These are scaled and saved with the
     `scaler_time` by `prepare_sequences`.

Labels and output
- The model outputs a 3-class softmax corresponding to the
  `IntradayTradeIndicator` created by `label_intraday_trade` in the
  feature module. The expected label mapping is:
    0 -> No Action
    1 -> Long Buy
    2 -> Short Sell

Notes
- `build_lstm_model` returns an uncompiled Keras `Model`. Compile with
  an appropriate optimizer and `loss='categorical_crossentropy'` for
  training with one-hot labels (see `train_model.train_model`).
- Input arrays fed to the model during training should have shapes:
    Xp: (batch_size, sequence_length, price_dim)
    Xi: (batch_size, sequence_length, indicator_dim)
    Xt: (batch_size, time_dim)

"""

from tensorflow.keras.layers import Input, LSTM, Dense, Concatenate
from tensorflow.keras.models import Model

def build_lstm_model(sequence_length, price_dim, indicator_dim, time_dim):
    """Create the LSTM model and document input/feature relationships.

    Args:
        sequence_length (int): number of timesteps per sequence (matches
            the `sequence_length` used in `prepare_sequences`).
        price_dim (int): number of features used in `price_input` (len of
            `price_features`).
        indicator_dim (int): number of features used in `indicator_input` (len of
            `indicator_features`).
        time_dim (int): number of non-sequential time features used in `time_input`.

    Returns:
        tf.keras.Model: an uncompiled Keras model accepting three inputs:
            [price_input, indicator_input, time_input] and producing a
            3-class softmax output matching `IntradayTradeIndicator` labels.

    Integration tips:
    - Ensure feature order and scaling used during `prepare_sequences` are
      preserved at inference (scalers are saved to `scalers/` by
      `prepare_sequences`).
    - If you change the label encoding in `feature_engineering`, update
      the model's output interpretation in `evaluate_model.evaluate_model`.
    """
    input_price = Input(shape=(sequence_length, price_dim), name="price_input")
    input_indicators = Input(shape=(sequence_length, indicator_dim), name="indicator_input")
    input_time = Input(shape=(time_dim,), name="time_input")

    lstm_price = LSTM(32, return_sequences=False)(input_price)
    lstm_indicators = LSTM(32, return_sequences=False)(input_indicators)

    merged = Concatenate()([lstm_price, lstm_indicators, input_time])
    dense = Dense(64, activation='relu')(merged)
    output = Dense(3, activation='softmax')(dense)

    model = Model(inputs=[input_price, input_indicators, input_time], outputs=output)
    return model
