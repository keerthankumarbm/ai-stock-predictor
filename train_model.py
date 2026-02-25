import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Load prepared data
X = np.load("X.npy")
y = np.load("y.npy")

# Build small LSTM model (lightweight)
model = Sequential()

model.add(LSTM(50, return_sequences=False, input_shape=(X.shape[1], 1)))
model.add(Dense(25))
model.add(Dense(1))

model.compile(optimizer='adam', loss='mean_squared_error')

# Train model
model.fit(X, y, batch_size=16, epochs=5)

# Save model
model.save("stock_model.h5")

print("Model trained and saved!")
