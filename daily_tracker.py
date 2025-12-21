import requests
import os
import pandas as pd # Now using pandas for the logic
from datetime import datetime

# 1. READ SECRETS
APP_ID = os.environ.get("ADZUNA_APP_ID")
APP_KEY = os.environ.get("ADZUNA_APP_KEY")
FILE_NAME = "job_market_history.csv"

def get_daily_job_count(title, country="us"):
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": title,
        "max_days_old": 1,
        "results_per_page": 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        return data.get('count', 0)
    except:
        return 0

def update_history(titles):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 2. Collect today's data in a dictionary
    # This is safer than a list because it links value to key (Title)
    current_data = {"Date": timestamp}
    
    print(f"--- Log for {timestamp} ---")
    for title in titles:
        count = get_daily_job_count(title)
        current_data[title] = count
        print(f"{title}: {count}")

    # 3. Load existing history safely
    if os.path.exists(FILE_NAME):
        try:
            history_df = pd.read_csv(FILE_NAME)
        except pd.errors.EmptyDataError:
            # Handle case where file exists but is empty
            history_df = pd.DataFrame()
    else:
        history_df = pd.DataFrame()

    # 4. Merge old history with new data
    # Create a 1-row DataFrame for today
    today_df = pd.DataFrame([current_data])
    
    # pd.concat is the "future-proof" magic.
    # It aligns columns by name. If 'today_df' has a new title, 
    # pandas adds that column to the whole dataset automatically.
    updated_df = pd.concat([history_df, today_df], ignore_index=True)
    
    # 5. Save back to CSV
    updated_df.to_csv(FILE_NAME, index=False)
    print(f"Saved to {FILE_NAME}")

if __name__ == "__main__":
    # You can now add/remove titles here freely!
    target_roles = [
        "Machine Learning Engineer", 
        "Data Scientist", 
        "Data Engineer",
        "AI Engineer",
        "Software Engineer",
        "AI Researcher",
        "Product Manager",
        "Technical Program Manager"
    ]
    
    if APP_ID and APP_KEY:
        update_history(target_roles)
    else:
        print("Error: API Keys not found.")