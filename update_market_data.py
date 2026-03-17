import pandas as pd
from datetime import datetime
from nepse_data_api import Nepse

print("Initializing NEPSE API Client...")
print("Handling authentication tokens silently in the background...\n")

try:
    # 1. Initialize the official API wrapper
    nepse = Nepse()
    
    # 2. Fetch the live index data directly from the source
    indices = nepse.get_nepse_index()
    
    latest_close = None
    
    # 3. Parse the data to find the main NEPSE index
    if isinstance(indices, list):
        for item in indices:
            if item.get('index') == 'NEPSE Index':
                # The API usually returns 'currentValue' or 'close'
                latest_close = item.get('currentValue') or item.get('close')
                break
    elif isinstance(indices, dict):
         latest_close = indices.get('currentValue') or indices.get('close') or indices.get('lastTradedPrice')
         
    # 4. Fallback safeguard
    if not latest_close:
        print("Raw Data Received:", indices)
        latest_close = float(input("\nCould not auto-parse. Please type the NEPSE closing value from the raw data above: "))
        
    latest_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"Successfully pulled live data:")
    print(f"Date: {latest_date}")
    print(f"NEPSE Close: {latest_close}\n")
    
    # --- 5. UPDATE YOUR HISTORICAL CSV ---
    print("Updating 'nepse_history.csv'...")
    history_df = pd.read_csv('nepse_history.csv')
    
    # Prevent duplicate entries if you run the script twice in one day
    if latest_date in history_df['Date'].values:
        print(f"Data for {latest_date} is already in your database. No update needed.")
    else:
        new_row = pd.DataFrame({
            'Date': [latest_date],
            'Index Value': [latest_close] 
        })
        # Append the new row to the historical dataset
        history_df = pd.concat([history_df, new_row], ignore_index=True)
        history_df.to_csv('nepse_history.csv', index=False)
        print(f"Success! Database updated with {latest_date} close.")

except Exception as e:
    print(f"Error fetching from NEPSE API: {e}")