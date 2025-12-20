import requests
import csv
import os
from datetime import datetime

# 1. READ SECRETS FROM ENVIRONMENT VARIABLES
# We will set these in GitHub Settings later
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
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if file exists to determine if we need a header
    file_exists = os.path.isfile(FILE_NAME)
    
    row = {"Date": today}
    print(f"--- Log for {today} ---")
    
    for title in titles:
        count = get_daily_job_count(title)
        row[title] = count
        print(f"{title}: {count}")

    with open(FILE_NAME, mode='a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Date"] + titles)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

if __name__ == "__main__":
    # You can change these titles to whatever you want
    target_roles = ["Machine Learning Engineer", "Data Scientist", "Data Engineer", 
                    "AI Researcher", "Software Engineer", "AI Engineer"]
    if APP_ID and APP_KEY:
        update_history(target_roles)
    else:
        print("Error: API Keys not found in environment variables.")