"""
model/evaluate_model.py

Evaluation utilities for visualizing classification performance of the
LSTM breakout predictor.

Expectations
- The model passed to `evaluate_model` should accept three inputs:
  [Xp, Xi, Xt] matching the arrays produced by `train_model.prepare_sequences`.
- `y_val` should be one-hot encoded with shape (n_samples, 3).
- Label ordering expected by this module is: [No Action, Long Buy, Short Sell]
  which matches `features/feature_engineering.label_intraday_trade` ->
  tf.keras.utils.to_categorical(..., num_classes=3)

Outputs
- A plotted confusion matrix and a printed classification report.
"""

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt

def evaluate_model(model, Xp_val, Xi_val, Xt_val, y_val):
    """Run prediction, plot confusion matrix and print classification report.

    Args:
        model: a compiled and trained Keras model.
        Xp_val, Xi_val, Xt_val: validation arrays matching training inputs.
        y_val: one-hot encoded true labels.
    """
    y_pred_probs = model.predict([Xp_val, Xi_val, Xt_val])
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = np.argmax(y_val, axis=1)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Action", "Long Buy", "Short Sell"])
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.show()

    report = classification_report(y_true, y_pred, target_names=["No Action", "Long Buy", "Short Sell"], zero_division=0)
    print("Classification Report:\n", report)
