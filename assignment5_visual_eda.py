import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("spacex_cleaned.csv")

# Style
sns.set(style="whitegrid")

# 1. Launches per year
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x='launch_year')
plt.title("Number of Launches Per Year")
plt.xlabel("Year")
plt.ylabel("Launch Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Success rate by year
success_rate = df.groupby('launch_year')['landing_success'].mean().reset_index()
success_rate['landing_success'] *= 100

plt.figure(figsize=(10, 5))
sns.lineplot(data=success_rate, x='launch_year', y='landing_success', marker="o")
plt.title("Landing Success Rate Over the Years")
plt.ylabel("Success Rate (%)")
plt.xlabel("Year")
plt.tight_layout()
plt.show()

# 3. Payload mass vs landing success
plt.figure(figsize=(10, 5))
sns.boxplot(data=df, x='landing_success', y='payload_mass_kg')
plt.title("Payload Mass vs Landing Success")
plt.xlabel("Landing Success (0 = Fail, 1 = Success)")
plt.ylabel("Payload Mass (kg)")
plt.tight_layout()
plt.show()

# 4. Launch site impact (top 5)
launch_cols = [col for col in df.columns if col.startswith("launch_site_")]
launch_counts = df[launch_cols].sum().sort_values(ascending=False).head(5)

plt.figure(figsize=(10, 5))
sns.barplot(x=launch_counts.index.str.replace("launch_site_", ""), y=launch_counts.values)
plt.title("Top 5 Launch Sites by Count")
plt.xlabel("Launch Site")
plt.ylabel("Number of Launches")
plt.tight_layout()
plt.show()
