import pandas as pd
import ta
import numpy as np

print("Initializing Quant Feature Engine...\n")

try:
    # 1. Load the raw historical data
    df = pd.read_csv('nepse_history.csv')
    
    # 2. Standardize the column names
    # Translating 'Index Value' to 'Close' so the math libraries understand it
    df.rename(columns={
        'Index Value': 'Close'
    }, inplace=True)
    
    # 3. Parse the dates and sort chronologically (oldest to newest)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date').reset_index(drop=True)

except FileNotFoundError:
    print("Error: 'nepse_history.csv' not found.")
    print("Please ensure the historical NEPSE data is saved in this folder.")
    exit()

print(f"Loaded {len(df)} days of historical NEPSE data.\n")

# --- 4. CALCULATING TECHNICAL INDICATORS (THE MATH) ---
print("Calculating technical indicators...")

# RSI (Relative Strength Index): 14-day window
df['RSI_14'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

# SMA (Simple Moving Average): 50-day macro trend
df['SMA_50'] = ta.trend.SMAIndicator(close=df['Close'], window=50).sma_indicator()

# Volatility (Bollinger Band Width): 20-day window
df['Bollinger_Width'] = ta.volatility.BollingerBands(close=df['Close'], window=20).bollinger_wband()

# --- 5. CREATING THE PREDICTION TARGET ---
# 1 = Market goes UP tomorrow (Bullish)
# 0 = Market goes DOWN tomorrow (Bearish)
df['Target_Next_Day_Up'] = (df['Close'].shift(-1) > df['Close']).astype(int)

# 6. Clean up the data
# Drop the rows that have NaN (Not a Number) because the 50-day SMA needs 50 days to calculate
df = df.dropna().reset_index(drop=True)

print("--- NEPSE Mathematical Matrix Generated ---")
# Print the last 5 days to verify the output
print(df[['Date', 'Close', 'RSI_14', 'SMA_50', 'Target_Next_Day_Up']].tail(5).to_string(index=False))

# 7. Save the engineered dataset
output_filename = 'nepse_quant_features.csv'
df.to_csv(output_filename, index=False)
print(f"\nSuccess. Feature matrix saved to '{output_filename}'")