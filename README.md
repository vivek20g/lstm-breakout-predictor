# lstm-breakout-predictor

Lightweight pipeline for preparing intraday trading features, training an LSTM-based
3-class breakout predictor (No Action / Long Buy / Short Sell), and evaluating results.

This repository contains feature engineering utilities, training/evaluation helpers,
and a small LSTM model definition implemented with TensorFlow / Keras.

## Repository structure

- `main.py` — orchestration script that runs the end-to-end pipeline (feature engineering → sequences → model training → evaluation → save model).
- `requirements.txt` — Python dependencies used by the project.
- `data/` — example input data (`ExecutionData_Sample.xlsx`). Replace with your execution logs (see notes below).
- `features/feature_engineering.py` — functions that add price dynamics, technical indicators (using `ta`) and create a 3-class label `IntradayTradeIndicator`.
- `model/lstm_model.py` — Keras model factory `build_lstm_model(...)` which returns an uncompiled LSTM model taking three inputs.
- `model/train_model.py` — utilities to scale features, build overlapping sequences, compute class weights, and run training.
- `model/evaluate_model.py` — simple evaluation helper that plots a confusion matrix and prints a classification report.

## Quick summary of how the pipeline works

1. Load raw execution log into a pandas DataFrame.
2. Run feature engineering:
   - `add_price_dynamics(df)` — adds price delta and volume-change features.
   - `add_technical_indicators(df)` — computes RSI, EMA, MACD, Bollinger band width, ATR, etc.
   - `label_intraday_trade(df)` — creates integer labels (0: No Action, 1: Long, 2: Short).
3. Select three groups of features and call `prepare_sequences(...)` to scale and construct overlapping sequences. Scalers are persisted to `scalers/` for inference.
4. Build the model with `build_lstm_model(...)`, compile it (example shown below), and train using `train_model(...)`.
5. Evaluate with `evaluate_model(...)` and save the trained model.

## Requirements

Install the project's Python dependencies (recommended to use a venv):

pip install -r requirements.txt

(See `requirements.txt` for pinned versions.)

## Example usage

1. Make sure your input Excel matches the column names expected by the feature functions. `features/feature_engineering.py` expects columns like:
   - `EntryPrice`, `ExitPrice`, `Open`, `High`, `Low`, `Close`, `MarketVolume`, `ExecutionDate`, `ProfitLoss`, `TradeDirection`.

2. Edit `main.py` if your input path or sheet name differ.

3. Compile the model before training (example):

```python
from model.lstm_model import build_lstm_model
model = build_lstm_model(sequence_length=9, price_dim=3, indicator_dim=7, time_dim=3)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
```

4. Run the pipeline:

python main.py

## Notes and caveats

- `features.label_intraday_trade` currently implements a simple rule: positive `ProfitLoss` → long/short based on `TradeDirection`; otherwise label 0. Adjust the labeling logic to match your trading definition of a "profitable" trade.
- Rolling technical indicators produce NaNs at the beginning of the series. The feature functions call `dropna()` in `label_intraday_trade` but you should verify cleaning and indexing for your dataset.
- `prepare_sequences` persists `MinMaxScaler` objects to `scalers/` — these must be used at inference time to apply the same scaling as training.
- Model outputs a softmax vector of length 3 matching the `IntradayTradeIndicator` encoding.

## How to add this project to a new GitHub repository

Option A — using GitHub CLI (`gh`):

1. In PowerShell, from the project root:

gh repo create vivek20g/lstm-breakout-predictor --public --source=. --remote=origin --push

Option B — manual (create repo on github.com then push):

1. Create a new empty repo named `lstm-breakout-predictor` on GitHub under your account `vivek20g`.
2. In PowerShell, from the project root:

git init
git add .
git commit -m "Initial import: LSTM breakout predictor"
git remote add origin https://github.com/vivek20g/lstm-breakout-predictor.git
git branch -M main
git push -u origin main

Notes:
- If you prefer SSH, use the SSH URL when running `git remote add`.
- If you want me to run these commands for you from this environment, provide permission and ensure Git is configured (and provide credentials or have `gh` authenticated). I cannot create the remote GitHub repository on your behalf without an authenticated GitHub CLI session or API token.

## License

Add a license file if you plan to open-source this repository (e.g. MIT).

## Contact

If you want me to push the code to your GitHub for you, tell me which method you prefer (GitHub CLI authenticated here, or provide a personal access token) and I will run the necessary commands. Otherwise follow the steps above to create and push the repository yourself.
