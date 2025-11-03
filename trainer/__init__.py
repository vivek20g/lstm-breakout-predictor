"""
trainer package — wrapper around the model training modules.
Exposes a simple API: Trainer class that uses model.pipeline.LSTMModelTrainer
"""
from model.pipeline import LSTMModelTrainer as Trainer

__all__ = ["Trainer"]
