import pandas as pd

# Load the raw SpaceX API dataset
df = pd.read_csv("spacex_full_data.csv")

print("Initial shape:", df.shape)

# Drop columns not useful for modeling
columns_to_drop = ['booster_version', 'landpad_name', 'date_utc']
df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

# Drop rows with critical missing values
df.dropna(subset=['landing_success', 'payload_mass_kg', 'orbit'], inplace=True)

# Fill remaining missing values if any (e.g., reused)
df['reused'].fillna(False, inplace=True)

# Convert booleans to integers
df['landing_success'] = df['landing_success'].astype(int)
df['reused'] = df['reused'].astype(int)

# One-hot encode categorical columns
categorical_cols = ['rocket_name', 'launch_site', 'orbit']
df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Save cleaned dataset
df.to_csv("spacex_cleaned.csv", index=False)

# Display info
print("Cleaned data saved to spacex_cleaned.csv")
print("Final shape:", df.shape)
print(df.head())
