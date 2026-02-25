import yfinance as yf
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

# Load trained model
model = load_model("stock_model.h5")


def predict_stock(stock_symbol):

    print(f"\nDownloading data for {stock_symbol}...")

    data = yf.download(stock_symbol, period="3mo")

    if len(data) < 60:
        print("❌ Not enough data")
        return

    # Use closing price
    close_data = data[['Close']].values

    # Normalize
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(close_data)

    # Last 60 days
    last_60 = scaled_data[-60:]
    X_test = np.reshape(last_60, (1, 60, 1))

    # Predict
    prediction = model.predict(X_test, verbose=0)
    predicted_price = scaler.inverse_transform(prediction)

    print("\n📊 Predicted Next Closing Price:")
    print(f"{stock_symbol} → ₹ {predicted_price[0][0]:.2f}")


# ---------------- MAIN ----------------
if __name__ == "__main__":

    print("\nAI STOCK PREDICTOR (Terminal Mode)")
    print("-----------------------------------")

    stock = input("Enter Stock Symbol (Example: TCS.NS): ").strip().upper()

    predict_stock(stock)
