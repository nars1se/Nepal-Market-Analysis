import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import pandas as pd
from datetime import datetime
import time

print("Waking up the Multi-Source NEPSE AI...\n")
analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
# SOurces to scrape with their specific rules for finding headlines

SOURCES = {
    "ShareSansar": {
        "url": "https://www.sharesansar.com/category/latest",
        "tag": "h4",
        "class_name": None # None means it just looks for the tag
    },
    "NepaliPaisa": {
        "url": "https://www.nepalipaisa.com/news",
        "tag": "h2", 
        "class_name": None 
    },
    "MeroLagani": {
        "url": "https://merolagani.com/NewsList.aspx",
        "tag": "h4", 
        "class_name": "media-heading" # Looks for <h4 class="media-heading">
    }
}

scraped_data = []
today = datetime.now().strftime("%Y-%m-%d")

print(f"--- Commencing Multi-Source Data Extraction for {today} ---")

# --- Loop through each website in our dictionary ---
for site_name, config in SOURCES.items():
    print(f"\n Connecting to {site_name}...")
    
    try:
        response = requests.get(config["url"], headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            if config["class_name"]:
                headlines = soup.find_all(config["tag"], class_=config["class_name"])
            else:
                headlines = soup.find_all(config["tag"])
            
            # Grab the top 5 headlines from this specific site to avoid clutter
            for headline in headlines[:5]:
                clean_title = headline.get_text(strip=True)
                
                # Skip empty titles
                if not clean_title:
                    continue
                    
                result = analyzer(clean_title)[0]
                mood = result['label'].upper()
                
                print(f"[{site_name}] {clean_title[:30]}... -> {mood}")
                
                scraped_data.append({
                    "Date": today,
                    "Source": site_name, # Track where the news came from
                    "Headline": clean_title,
                    "Sentiment": mood,
                    "Confidence_Score": round(result['score'], 4)
                })
        else:
             print(f" Failed to load {site_name}. Code: {response.status_code}")
             
    except Exception as e:
        print(f" Error scraping {site_name}: {e}")
        
    time.sleep(2)

# Save the combined data
df = pd.DataFrame(scraped_data)
df.to_csv("nepse_daily_sentiment.csv", index=False)
print("\n Multi-Source Extraction Complete. Data Saved!")