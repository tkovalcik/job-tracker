# 📈 Automated Job Market Tracker
![Daily Job Market Tracker](https://github.com/tkovalcik/job-tracker/actions/workflows/daily_job_schedule.yml/badge.svg)

A daily data pipeline that tracks the volume of new job postings for various tech roles roles.

## 📊 Live Trends (Last 30 Days)
![Daily Job Market Trends](job_market_trends.png)

### 🚀 [Click Here for the Interactive Dashboard](https://tkovalcik.github.io/job-tracker/)
Use the interactive dashboard to:
- Filter specific job titles (click legends to toggle)
- Zoom in on specific dates
- Hover to see exact numbers

## 🛠️ How it Works
1. **Scraper:** A Python script hits the Adzuna API every 24 hours.
2. **Analysis:** It calculates the volume of new postings for for several job titles.
3. **Visualization:** Matplotlib generates the trend line above.
4. **Automation:** GitHub Actions handles the scheduling, execution, and committing of new data.

## 📂 Data
The data is obtained from [The Adzuna API](http://www.adzuna.co.uk/). The raw historical data obtained from the API is available in [job_market_history.csv](job_market_history.csv).

