Nepal Market Analysis (NEPSE)

An automated quantitative trading data pipeline and machine learning predictor for the Nepal Stock Exchange (NEPSE). This project fetches live market data, engineers technical indicators, and trains a baseline classification model to predict the next day's market direction.

🧠 System Architecture

This project is built on a 3-step daily automated pipeline:

Live Market Data Fetcher (update_market_data.py):

Uses the nepse-data-api to bypass firewalls and fetch the live daily closing price of the NEPSE index.

Automatically appends the latest closing data to the local historical database (nepse_history.csv).

Feature Engineering Engine (quant_features.py):

Uses the ta (Technical Analysis) library to transform raw closing prices into mathematical momentum, trend, and volatility indicators.

Features Generated: 14-day RSI, 50-day SMA, 20-day Bollinger Band Width.

Target Variable: Calculates a strict time-shifted binary Target_Next_Day_Up label (1 for Up, 0 for Down) to train the predictive model without data leakage.

Machine Learning Predictor (train_model.py):

Trains a RandomForestClassifier on the engineered mathematical matrix.

Uses strict time-series splitting (shuffle=False) during backtesting to simulate real-world trading constraints.

Outputs a probability-weighted prediction for tomorrow's market movement based on today's live data.

⚙️ Prerequisites & Installation

To run this pipeline, you need Python 3.8+ installed on your machine.

Clone the repository:

git clone [https://github.com/yourusername/nepse-quant-bot.git](https://github.com/yourusername/Nepal-Market-Analysis.git)
cd nepse-quant-bot


Install the required dependencies:

pip install pandas numpy scikit-learn ta nepse-data-api


🚀 Usage

The pipeline is designed to be run sequentially after the NEPSE market closes for the day.

# 1. Update the database with today's live close
python update_market_data.py

# 2. Recalculate technical indicators and generate the feature matrix
python quant_features.py

# 3. Train the Random Forest and generate tomorrow's prediction
python train_model.py


🚧 Current Status & Roadmap

[x] Establish live API data connection for daily updates.

[x] Build mathematical feature matrix (RSI, SMA, Bollinger Bands).

[x] Train baseline Machine Learning model (Random Forest).

[ ] Upcoming: Integrate NLP Sentiment Analysis to process daily financial news and combine it with the technical matrix to improve model accuracy beyond the baseline.
