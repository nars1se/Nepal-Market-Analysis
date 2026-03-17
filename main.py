import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import pandas as pd
from datetime import datetime

print("Loading AI Model and Scraper...\n")

analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")

url = "https://www.sharesansar.com/category/latest"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    headlines = soup.find_all('h4')
    
    # --- NEW: Create an empty list to store our data ---
    scraped_data = []
    
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"--- Analyzing NEPSE News for {today} ---")
    
    for i, headline in enumerate(headlines[:15], start=1):
        clean_title = headline.get_text(strip=True)
        result = analyzer(clean_title)[0] 
        
        mood = result['label'].upper()
        confidence = result['score']
        
        print(f"Processed: {clean_title[:30]}... -> {mood}")
        
        # --- NEW: Save the results into a dictionary, then add to our list ---
        scraped_data.append({
            "Date": today,
            "Headline": clean_title,
            "Sentiment": mood,
            "Confidence_Score": round(confidence, 4)
        })

    # --- NEW: Convert the list into a Pandas DataFrame (like a virtual spreadsheet) ---
    df = pd.DataFrame(scraped_data)
    
    # Save the spreadsheet to a CSV file in the same folder as this script
    csv_filename = "nepse_daily_sentiment.csv"
    df.to_csv(csv_filename, index=False)
    
    print(f"\n✅ Success! Data saved to {csv_filename}")

else:
    print(f"Failed to connect. Error code: {response.status_code}")