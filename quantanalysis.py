import pandas as pd


# 1. Load the data you scraped earlier
try:
    df = pd.read_csv("nepse_daily_sentiment.csv")
except FileNotFoundError:
    print("Error: Could not find the CSV file. Did you run the scraper first?")
    exit()

# 2. Feature Engineering: Convert text to math
def calculate_score(row):
    if row['Sentiment'] == 'POSITIVE':
        return row['Confidence_Score']
    elif row['Sentiment'] == 'NEGATIVE':
        return -row['Confidence_Score']
    else:
        return 0.0

# Apply our math formula to create a new column in the spreadsheet
df['Math_Score'] = df.apply(calculate_score, axis=1)

# 3. Calculate the Daily "Market Mood"
# We group all articles by Date and find the average sentiment score
daily_mood = df.groupby('Date')['Math_Score'].mean().reset_index()
daily_mood.rename(columns={'Math_Score': 'Average_Mood'}, inplace=True)

print("--- Daily NEPSE Sentiment Scores ---")
print(daily_mood.to_string(index=False))
print("-" * 36)

# 4. The Trading Logic (The Quant Signal)
# Grab today's average score
todays_score = daily_mood['Average_Mood'].iloc[0]

print("\n ALGORITHMIC TRADING SIGNAL:")
if todays_score > 0.15:
    print(f"BULLISH (Score: {todays_score:.2f}) -> Positive market sentimient. Nepse could rise.")
elif todays_score < -0.15:
    print(f"BEARISH (Score: {todays_score:.2f}) -> Negative market sentiment. Nepse could be volatile and fall.")
else:
    print(f"NEUTRAL (Score: {todays_score:.2f}) -> Undecided. No clear news.")