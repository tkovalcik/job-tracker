import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import timedelta
import os

FILE_NAME = "job_market_history.csv"
STATIC_GRAPH_NAME = "job_market_trends.png"
INTERACTIVE_GRAPH_NAME = "index.html"

def generate_graphs():
    if not os.path.exists(FILE_NAME):
        print("No data file found.")
        return

    try:
        df = pd.read_csv(FILE_NAME)
    except pd.errors.EmptyDataError:
        print("CSV is empty.")
        return

    # 1. Convert Date to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], format='mixed', errors='coerce')
    
    # 2. AGGREGATION LOGIC (Collapse multiple runs per day)
    # Create a temporary 'Day' column just for grouping
    df['Date'] = df['Date'].dt.date
    
    # Group by 'Day' and take the .last() entry for every column
    # This keeps the last timestamp of that day and the last data values
    df_daily = df.groupby('Date').last().reset_index(drop=False)

    # 3. FILTER LOGIC (Show only roles active in the most recent run)
    # Get the last row of data
    last_row = df_daily.iloc[-1]
    
    # Identify columns that are NOT 'Date' and have valid data (not NaN) in the last row
    active_roles = [col for col in df_daily.columns 
                    if col != 'Date' and pd.notna(last_row[col])]
    
    print(f"Active roles found: {active_roles}")

    # Calculate Date Range for Plotting (+/- 5 Days)
    min_date = df_daily['Date'].min() - timedelta(days=5)
    max_date = df_daily['Date'].max() + timedelta(days=5)

    # --- PART 1: STATIC MATPLOTLIB IMAGE ---
    plt.figure(figsize=(10, 6))
    
    # Loop ONLY through the active_roles list
    for column in active_roles:
        plt.plot(df_daily['Date'], df_daily[column], marker='o', label=column)

    plt.title('Daily Job Market Trends (Last Update)')
    plt.xlabel('Date')
    plt.ylabel('New Postings (24h)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlim(min_date, max_date)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(STATIC_GRAPH_NAME)
    print(f"Static graph saved to {STATIC_GRAPH_NAME}")

    # --- PART 2: INTERACTIVE PLOTLY HTML ---
    # We filter the dataframe first to only include Date + Active Roles
    plot_cols = ['Date'] + active_roles
    df_filtered = df_daily[plot_cols]
    
    df_long = df_filtered.melt(id_vars=['Date'], var_name='Role', value_name='Postings')

    fig = px.line(df_long, x='Date', y='Postings', color='Role', markers=True,
                  title='Interactive Job Market Tracker')

    fig.update_xaxes(range=[min_date, max_date])
    fig.write_html(INTERACTIVE_GRAPH_NAME)
    print(f"Interactive dashboard saved to {INTERACTIVE_GRAPH_NAME}")

if __name__ == "__main__":
    generate_graphs()