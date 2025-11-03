# lstm-breakout-predictor

Lightweight pipeline to prepare intraday trading features, train an LSTM-based
3-class breakout classifier (No Action / Long / Short), and evaluate results.

Highlights
- Feature engineering in `features/feature_engineering.py` (price deltas, RSI, EMA, MACD, ATR, etc.).
- Sequence preparation, scaling and training utilities in `model/`.
- `model.LSTMModelTrainer` provides a compact API for preprocessing → training → evaluation → save.

Quick start

1. Create and activate a virtual environment, then install dependencies:

   pip install -r requirements.txt

2. Prepare your data

   Place your execution log (Excel/CSV) in `data/`. The feature functions expect columns such as:
   `EntryPrice, ExitPrice, Open, High, Low, Close, MarketVolume, ExecutionDate, ProfitLoss, TradeDirection`.

3. Run the example pipeline

   python main.py

   `main.py` runs feature engineering, prepares sequences (saves scalers to `scalers/`), builds and trains the model and saves it to `model/daytrading_breakout_model.keras`.

API (for scripts / interactive use)

- Preprocessing + training helper (recommended):

```py
from model import LSTMModelTrainer
trainer = LSTMModelTrainer(sequence_length=9)
Xp, Xi, Xt, y = trainer.preprocess(df, price_features, indicator_features, time_features)
trainer.build_model(price_dim=len(price_features), indicator_dim=len(indicator_features), time_dim=len(time_features))
trainer.compile()
trainer.fit(Xp, Xi, Xt, y)
trainer.save()
```

- Low-level helpers are available in `model` and `features` modules.

Notes
- `prepare_sequences` persists `MinMaxScaler` objects in `scalers/`; use them at inference to ensure consistent scaling.
- Rolling indicators create NaNs at the start of series — ensure data is cleaned (`dropna()`) before training.
- `features.label_intraday_trade` uses a simple profit-based rule: positive `ProfitLoss` -> label 1 (LONG) or 2 (SHORT); otherwise 0. Adjust as needed.

Contributing
- Open issues or PRs. Keep changes small and add tests where appropriate.

License
- This project is available under the MIT License — see `LICENSE`.

Contact
- Repository: https://github.com/vivek20g/lstm-breakout-predictor
