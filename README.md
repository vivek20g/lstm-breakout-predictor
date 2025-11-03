# lstm-breakout-predictor

Lightweight pipeline to prepare intraday trading features, train an LSTM-based
3-class breakout classifier (No Action / Long / Short), and evaluate results.

Highlights
- Feature engineering utilities in `features/feature_engineering.py`.
- `FeatureEngineer` wrapper in `features/engineer.py` for a single-step transform.
- Sequence preparation, scaling and training utilities in `model/`.
- `model.LSTMModelTrainer` provides a compact API for preprocessing → training → evaluation → save.

Quick start

1. Create and activate a virtual environment and install dependencies:

   pip install -r requirements.txt

2. Prepare your data

   Place your execution log (Excel/CSV) in `data/`. Expected columns include:
   `EntryPrice, ExitPrice, Open, High, Low, Close, MarketVolume, ExecutionDate, ProfitLoss, TradeDirection`.

3. Run the example pipeline

   python main.py

   This will run feature engineering (via `FeatureEngineer`), prepare sequences (scalers saved to `scalers/`), train an LSTM, evaluate and save the model to `model/daytrading_breakout_model.keras`.

API (recommended usage)

- High-level programmatic flow:

```py
from features import FeatureEngineer
from model import LSTMModelTrainer

fe = FeatureEngineer()
df = fe.run(df)

price_features = ['Entry_vs_PrevClose', 'EntryPriceChange', 'volatility']
indicator_features = ['EMA_10', 'EMA_20', 'MA50', 'BB_Width', 'RSI', 'Momentum', 'ATR']
time_features = ['HourOfDay', 'OrderMonth', 'GoldenCrossover']

trainer = LSTMModelTrainer(sequence_length=9)
Xp, Xi, Xt, y = trainer.preprocess(df, price_features, indicator_features, time_features)
trainer.build_model(len(price_features), len(indicator_features), len(time_features))
trainer.compile()
trainer.fit(Xp, Xi, Xt, y)
trainer.save()
```

- Low-level helpers remain available for more control in `features` and `model` packages.

Notes
- `prepare_sequences` persists `MinMaxScaler` objects to `scalers/` — reuse them at inference to preserve scaling.
- Rolling indicators create NaNs at the start of series — ensure data is cleaned (`dropna()`) before training.
- `label_intraday_trade` uses a simple profit-based rule: positive `ProfitLoss` -> label 1 (LONG) or 2 (SHORT); otherwise 0. Adjust the logic to match your business rules.

Repository files of interest
- `main.py` — example script using `FeatureEngineer` + `LSTMModelTrainer`.
- `features/feature_engineering.py` — individual feature functions.
- `features/engineer.py` — FeatureEngineer wrapper.
- `model/` — model factory, training utilities, evaluation and pipeline.

Contributing
- PRs welcome. Keep changes small and add tests where appropriate.

License
- MIT (see `LICENSE`).

Repository
- https://github.com/vivek20g/lstm-breakout-predictor
