"""
model/evaluate_trainer.py

Simple evaluation helpers.
"""

import numpy as np
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report
import matplotlib.pyplot as plt


def evaluate_model(model, Xp_val, Xi_val, Xt_val, y_val):
    y_pred_probs = trainer.predict([Xp_val, Xi_val, Xt_val])
    y_pred = np.argmax(y_pred_probs, axis=1)
    y_true = np.argmax(y_val, axis=1)

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["No Action", "Long Buy", "Short Sell"])
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix")
    plt.show()

    report = classification_report(y_true, y_pred, target_names=["No Action", "Long Buy", "Short Sell"], zero_division=0)
    print(report)

