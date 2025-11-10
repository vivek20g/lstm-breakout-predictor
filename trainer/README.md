# Trainer

LSTM-based neural network training pipeline for breakout trading signal prediction.

## Overview

The trainer builds and trains deep learning models to predict trading breakouts from historical execution data:
- Loads simulated or real trading datasets from Excel/CSV files
- Performs feature engineering with technical indicators
- Creates sequential data for LSTM input
- Trains multi-input LSTM models with price, indicator, and time features
- Saves trained models and scalers for inference

## Key Components

- **`lstm_model.py`** - LSTM architecture definition and model building
- **`train_from_file.py`** - High-level training interface from file input
- **`train_model.py`** - Core training logic and model compilation
- **`pipeline.py`** - End-to-end training pipeline orchestration
- **`evaluate_model.py`** - Model evaluation and performance metrics

## Model Architecture

- **Multi-input LSTM** with three branches:
  - Price features (OHLCV sequences)
  - Technical indicators (RSI, MACD, EMA, etc.)
  - Time features (month, hour of day)
- **Output**: 3-class classification (No Action, LONG, SHORT)

## Features

The model uses these technical indicators:
- Price relationships (entry vs previous close, price changes)
- Moving averages (EMA 10/20, MA 50)  
- Momentum indicators (RSI, MACD, ROC)
- Volatility measures (Bollinger Bands, ATR)
- Time-based features (month, hour)

## Usage

```python
from trainer.train_from_file import train_from_file

# Train model from simulated dataset
train_from_file("simulator/output/simulated_trades.xlsx")
```

## Output

- **Trained model**: Saved as Keras .h5 or .keras file
- **Scalers**: Separate scalers for price, indicator, and time features  
- **Evaluation metrics**: Classification report and performance stats

The trained model can be used for real-time breakout signal generation.

