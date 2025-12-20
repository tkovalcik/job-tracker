import pandas as pd
import matplotlib.pyplot as plt
import os

FILE_NAME = "job_market_history.csv"
GRAPH_NAME = "job_market_trends.png"

def generate_graph():
    # 1. Safety check: Ensure the data file exists
    if not os.path.exists(FILE_NAME):
        print("No data file found to plot.")
        return

    # 2. Load data
    try:
        df = pd.read_csv(FILE_NAME)
    except pd.errors.EmptyDataError:
        print("CSV is empty, skipping plot.")
        return

    # 3. Process Data
    # Convert 'Date' string to actual datetime objects for better plotting
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set the plot size (Width, Height)
    plt.figure(figsize=(10, 6))

    # 4. Plot each job title as a separate line
    for column in df.columns:
        if column != 'Date':
            plt.plot(df['Date'], df[column], marker='o', label=column)

    # 5. Styling
    plt.title('Daily Job Market Trends')
    plt.xlabel('Date')
    plt.ylabel('New Postings (24h)')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45) # Rotate dates so they don't overlap
    plt.tight_layout()      # Adjust layout to fit everything nicely

    # 6. Save the image
    plt.savefig(GRAPH_NAME)
    print(f"Graph saved to {GRAPH_NAME}")

if __name__ == "__main__":
    generate_graph()