import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import timedelta
import os

FILE_NAME = "job_market_history.csv"
STATIC_GRAPH_NAME = "job_market_trends.png"
INTERACTIVE_GRAPH_NAME = "index.html" # Standard name for web entry points

def generate_graphs():
    if not os.path.exists(FILE_NAME):
        print("No data file found.")
        return

    try:
        df = pd.read_csv(FILE_NAME)
    except pd.errors.EmptyDataError:
        print("CSV is empty.")
        return

    # Convert Date to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Calculate Date Range with +/- 5 Days Buffer
    min_date = df['Date'].min() - timedelta(days=5)
    max_date = df['Date'].max() + timedelta(days=5)

    # --- PART 1: STATIC MATPLOTLIB IMAGE (For README) ---
    plt.figure(figsize=(10, 6))
    for column in df.columns:
        if column != 'Date':
            plt.plot(df['Date'], df[column], marker='o', label=column)

    plt.title('Daily Job Market Trends')
    plt.xlabel('Date')
    plt.ylabel('New Postings')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    
    # Apply the 5-day buffer
    plt.xlim(min_date, max_date)
    
    plt.tight_layout()
    plt.savefig(STATIC_GRAPH_NAME)
    print(f"Static graph saved to {STATIC_GRAPH_NAME}")

    # --- PART 2: INTERACTIVE PLOTLY HTML (For Website) ---
    # We need to 'melt' the dataframe to make it Plotly-friendly
    # (Turning wide columns into a long format)
    df_long = df.melt(id_vars=['Date'], var_name='Role', value_name='Postings')

    fig = px.line(df_long, x='Date', y='Postings', color='Role', markers=True,
                  title='Interactive Job Market Tracker')

    # Apply the 5-day buffer to the interactive chart too
    fig.update_xaxes(range=[min_date, max_date])
    
    # Save as HTML
    fig.write_html(INTERACTIVE_GRAPH_NAME)
    print(f"Interactive dashboard saved to {INTERACTIVE_GRAPH_NAME}")

if __name__ == "__main__":
    generate_graphs()