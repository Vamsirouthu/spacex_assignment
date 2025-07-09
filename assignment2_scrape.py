import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm

# Wikipedia URL to scrape
URL = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"

# Fetch page content
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# Find all launch tables (wikitable class)
tables = soup.find_all("table", class_="wikitable")

launch_data = []

print("Scraping tables from Wikipedia...")
for idx, table in enumerate(tqdm(tables)):
    try:
        df = pd.read_html(str(table))[0]

        # Skip empty or non-relevant tables
        if df.shape[1] < 5:
            continue

        df['source_table'] = idx  # Track source table
        launch_data.append(df)

    except Exception as e:
        print(f"Skipping table {idx} due to error: {e}")
        continue

# Combine all launch tables into one DataFrame
combined_df = pd.concat(launch_data, ignore_index=True)

# Save to CSV
combined_df.to_csv("spacex_wiki_launch_data.csv", index=False)
print("Data saved to spacex_wiki_launch_data.csv")
print(f"Total rows collected: {len(combined_df)}")
print(combined_df.head())
