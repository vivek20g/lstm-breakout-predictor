"""
model/train_model.py

Training utilities that convert a feature-engineered dataframe into
sequence arrays consumable by the LSTM model and run training.

Relationships to other modules
- Expects `df` to contain columns produced by `features/feature_engineering.py`.
- `prepare_sequences` saves fitted scalers to the `scalers/` directory; these
  are required at inference time to transform incoming raw features.
- The returned arrays match the inputs required by `model.lstm_model.build_lstm_model`:
  (Xp: price sequences, Xi: indicator sequences, Xt: time features) and the
  labels are returned as one-hot encoded (3 classes) suitable for training.
"""

import numpy as np
from sklearn.preprocessing import MinMaxScaler
import joblib
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping, LearningRateScheduler

def prepare_sequences(df, price_features, indicator_features, time_features, sequence_length):
    """Scale features and build overlapping sequences for training.

    Args:
        df: pandas DataFrame containing the raw and engineered features.
        price_features: list of column names used for price_input.
        indicator_features: list of column names used for indicator_input.
        time_features: list of column names used for time_input (non-sequential).
        sequence_length: number of timesteps per training example.

    Returns:
        Xp: numpy array of shape (n_samples, sequence_length, len(price_features))
        Xi: numpy array of shape (n_samples, sequence_length, len(indicator_features))
        Xt: numpy array of shape (n_samples, len(time_features))
        y: one-hot encoded labels with shape (n_samples, 3)

    Notes:
    - This function persists MinMaxScalers to `scalers/` so the same
      transformation can be applied at inference time.
    - The caller should ensure `df` has been cleaned for NaNs produced by
      rolling indicator calculations in `feature_engineering.py`.
    """
    scaler_price = MinMaxScaler()
    scaler_indicators = MinMaxScaler()
    scaler_time = MinMaxScaler()

    X_price = scaler_price.fit_transform(df[price_features])
    X_indicators = scaler_indicators.fit_transform(df[indicator_features])
    X_time = scaler_time.fit_transform(df[time_features])

    joblib.dump(scaler_price, "scalers/scaler_price.pkl")
    joblib.dump(scaler_indicators, "scalers/scaler_indicators.pkl")
    joblib.dump(scaler_time, "scalers/scaler_time.pkl")

    Xp, Xi, Xt, y = [], [], [], []
    for i in range(len(df) - sequence_length):
        Xp.append(X_price[i:i+sequence_length])
        Xi.append(X_indicators[i:i+sequence_length])
        Xt.append(X_time[i+sequence_length])
        y.append(df['IntradayTradeIndicator'].iloc[i+sequence_length])

    return np.array(Xp), np.array(Xi), np.array(Xt), tf.keras.utils.to_categorical(y, num_classes=3)

def compute_class_weights(y_train):
    """Compute balanced class weights from one-hot encoded labels.

    Returns a dict mapping class index to weight for use in `model.fit(..., class_weight=...)`.
    """
    from sklearn.utils import class_weight
    y_labels = np.argmax(y_train, axis=1)
    weights = class_weight.compute_class_weight('balanced', classes=np.unique(y_labels), y=y_labels)
    return dict(enumerate(weights))

def train_model(model, Xp, Xi, Xt, y_train, class_weights):
    """Train the compiled Keras model using prepared sequences.

    Uses EarlyStopping and a simple learning-rate schedule. Returns the Keras
    History object for inspection.
    """
    def scheduler(epoch, lr):
        return lr if epoch < 10 else lr * 0.5 if epoch < 30 else lr * 0.1

    callbacks = [
        EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True),
        LearningRateScheduler(scheduler)
    ]

    history = model.fit(
        [Xp, Xi, Xt],
        y_train,
        epochs=100,
        batch_size=32,
        validation_split=0.3,
        class_weight=class_weights,
        callbacks=callbacks
    )
    return history
