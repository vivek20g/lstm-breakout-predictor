# lstm-breakout-predictor

Small monorepo that separates simulated data generation (simulator/) from model training (trainer/).

Summary
- simulator/: produces synthetic execution logs from historical price Excel and spread matrices. Writes output Excel (with metadata) to `simulator/output/`.
- trainer/: model training pipeline based on an LSTM. Provides `train_from_file` helper to train from a CSV/XLSX produced by the simulator.
- features/: feature engineering utilities used before training.
- main.py: simple orchestrator to run generation and/or training from the repo root.

Quick start
1. Create a virtual environment and install dependencies

   python -m venv .venv; .\.venv\Scripts\Activate.ps1; python -m pip install -r requirements.txt

2. Generate simulated data (default reads `simulator/data/NiftyPrice.xlsx`)

   python main.py --generate

   Output: `simulator/output/simulated_trades.xlsx` and metadata `simulator/output/simulated_trades.xlsx.meta.json`.

3. Train the model on the generated dataset

   python main.py --train

   The trainer loads the dataset, runs feature engineering, prepares sequences, trains the LSTM and saves the model under `trainer/` defaults.

Programmatic usage
- Generate dataset from code

```py
from simulator import generate_dataset
generate_dataset('simulator/data/NiftyPrice.xlsx', 'simulator/output/simulated_trades.xlsx')
```

- Train from a dataset file

```py
from trainer.train_from_file import train_from_file
train_from_file('simulator/output/simulated_trades.xlsx')
```

Notes and conventions
- Simulator writes an accompanying `.meta.json` with creation timestamp, source, seed and row count for reproducibility.
- Trainer and features are decoupled: trainer expects a file path (CSV/XLSX). This makes it easy to iterate on the simulator without changing training code.
- Keep `simulator/data/` for small example inputs (spread matrices, price Excel). For large datasets, store externally and update paths.

Where to look in the repo
- `simulator/` — generation code, CLI and example data
- `trainer/` — LSTM model, training utilities and `train_from_file.py` helper
- `features/` — feature engineering
- `main.py` — orchestrator that composes simulator + trainer

License
- MIT
