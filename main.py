"""main.py — pipeline orchestration (concise)."""

import pandas as pd
from features import add_price_dynamics, add_technical_indicators, label_intraday_trade
from model import build_lstm_model, prepare_sequences, compute_class_weights, train_model, evaluate_model


def main():
    df = pd.read_excel("data/ExecutionData_Sample.xlsx", engine="openpyxl")
    df = df.sort_values(by="ExecutionDate")

    df = add_price_dynamics(df)
    df = add_technical_indicators(df)
    df = label_intraday_trade(df)

    price_features = ['Entry_vs_PrevClose', 'EntryPriceChange', 'volatility']
    indicator_features = ['EMA_10', 'EMA_20', 'MA50', 'BB_Width', 'RSI', 'Momentum', 'ATR']
    time_features = ['HourOfDay', 'OrderMonth', 'GoldenCrossover']

    sequence_length = 9
    Xp, Xi, Xt, y_train = prepare_sequences(df, price_features, indicator_features, time_features, sequence_length)

    class_weights = compute_class_weights(y_train)

    model = build_lstm_model(sequence_length, len(price_features), len(indicator_features), len(time_features))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    history = train_model(model, Xp, Xi, Xt, y_train, class_weights)

    val_size = int(len(y_train) * 0.3)
    evaluate_model(model, Xp[-val_size:], Xi[-val_size:], Xt[-val_size:], y_train[-val_size:])

    model.save("model/daytrading_breakout_model.keras")


if __name__ == "__main__":
    main()