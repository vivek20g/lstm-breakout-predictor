"""main.py — run pipeline using the LSTMModelTrainer and FeatureEngineer."""

import pandas as pd
from features import FeatureEngineer
from model import LSTMModelTrainer


def main():
    df = pd.read_excel("data/ExecutionData_Sample.xlsx", engine="openpyxl")
    df = df.sort_values(by="ExecutionDate")

    fe = FeatureEngineer()
    df = fe.run(df)

    price_features = ['Entry_vs_PrevClose', 'EntryPriceChange', 'volatility']
    indicator_features = ['EMA_10', 'EMA_20', 'MA50', 'BB_Width', 'RSI', 'Momentum', 'ATR']
    time_features = ['HourOfDay', 'OrderMonth', 'GoldenCrossover']

    sequence_length = 9
    trainer = LSTMModelTrainer(sequence_length=sequence_length)

    Xp, Xi, Xt, y = trainer.preprocess(df, price_features, indicator_features, time_features)

    trainer.build_model(price_dim=len(price_features), indicator_dim=len(indicator_features), time_dim=len(time_features))
    trainer.compile()

    trainer.fit(Xp, Xi, Xt, y)

    val_size = int(len(y) * 0.3)
    trainer.evaluate(Xp[-val_size:], Xi[-val_size:], Xt[-val_size:], y[-val_size:])

    trainer.save()


if __name__ == "__main__":
    main()