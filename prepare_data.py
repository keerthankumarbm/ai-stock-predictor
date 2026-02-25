import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Skip the second row (ticker row)
df = pd.read_csv("stock_data.csv", skiprows=[1])

# Keep only closing price
df = df[['Close']]

# Convert to numeric (force remove text)
df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

# Remove any invalid rows
df.dropna(inplace=True)

data = df.values

# Scale
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(data)

# Create sequences
X = []
y = []

for i in range(60, len(scaled_data)):
    X.append(scaled_data[i-60:i, 0])
    y.append(scaled_data[i, 0])

X, y = np.array(X), np.array(y)

# reshape for LSTM
X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# Save
np.save("X.npy", X)
np.save("y.npy", y)

print("Data prepared successfully")
print("X shape:", X.shape)
print("y shape:", y.shape)
