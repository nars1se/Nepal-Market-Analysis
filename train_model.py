import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Initializing Quant AI Machine Learning Model...\n")

# 1. Load the Math Matrix we built earlier
try:
    df = pd.read_csv('nepse_quant_features.csv')
except FileNotFoundError:
    print("Error: 'nepse_quant_features.csv' not found. Run quant_features.py first.")
    exit()

# 2. Separate "Today" from "History"
# The very last row is today's live data. We don't know tomorrow's outcome yet!
# We must separate it from the training data.
train_df = df.iloc[:-1] 
today_data = df.iloc[-1:]

# 3. Define the Features (The X Variables) and the Target (The Y Variable)
features = ['Close', 'RSI_14', 'SMA_50', 'Bollinger_Width']
X = train_df[features]
y = train_df['Target_Next_Day_Up']

# 4. Split the historical data into a "Study Guide" (Train) and a "Final Exam" (Test)
# VERY IMPORTANT: shuffle=False ensures we don't cheat by looking at the future to predict the past.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 5. Train the Random Forest
print("Training the Random Forest algorithm on historical NEPSE data...")
# n_estimators=100 means we are building 100 different decision trees and letting them vote
model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=5)
model.fit(X_train, y_train)

# 6. Grade the AI's "Final Exam"
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Backtest Accuracy on unseen historical data: {accuracy * 100:.2f}%\n")

# 7. THE REAL TEST: Predict Tomorrow!
print("--- PREDICTING TOMORROW'S MARKET MOVEMENT ---")

# We give the AI today's live data
today_X = today_data[features]

# The AI makes its prediction (1 = Up, 0 = Down)
tomorrow_prediction = model.predict(today_X)[0]

# We ask the AI how confident it is in its prediction
confidence = model.predict_proba(today_X)[0][tomorrow_prediction]

if tomorrow_prediction == 1:
    print(f"BULLISH: The AI predicts the NEPSE will close HIGHER tomorrow.")
else:
    print(f"BEARISH: The AI predicts the NEPSE will close LOWER tomorrow.")

print(f"Model Confidence: {confidence * 100:.2f}%")
print("---------------------------------------------")