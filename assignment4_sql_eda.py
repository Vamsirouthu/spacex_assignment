import duckdb
import pandas as pd

# Load cleaned CSV
df = pd.read_csv("spacex_cleaned.csv")

# Create DuckDB in-memory connection
con = duckdb.connect()

# Register DataFrame as a table
con.register("launches", df)

# Query 1: Number of launches per year
query1 = """
SELECT launch_year, COUNT(*) AS total_launches
FROM launches
GROUP BY launch_year
ORDER BY launch_year
"""
print("Launches per year:")
print(con.execute(query1).fetchdf())

# Query 2: Landing success rate per year
query2 = """
SELECT launch_year,
       COUNT(*) AS total,
       SUM(landing_success) AS successful,
       ROUND(100.0 * SUM(landing_success) / COUNT(*), 2) AS success_rate
FROM launches
GROUP BY launch_year
ORDER BY launch_year
"""
print("\n Landing success rate per year:")
print(con.execute(query2).fetchdf())

# Query 3: Payload mass vs landing success
query3 = """
SELECT payload_mass_kg, landing_success
FROM launches
ORDER BY payload_mass_kg
"""
print("\n Payload mass vs landing success (sample):")
print(con.execute(query3).fetchdf().head())

# Query 4: Best launch sites by success rate
query4 = """
SELECT 
    column_name,
    ROUND(100.0 * SUM(landing_success) / COUNT(*), 2) AS success_rate,
    COUNT(*) AS total_launches
FROM (
    SELECT *,
           unnest(regexp_extract_all(column_name, '[^_]+$')) AS column_name
    FROM launches
    UNPIVOT (value FOR column_name IN (*))
    WHERE column_name LIKE 'launch_site_%'
) 
WHERE value = 1
GROUP BY column_name
ORDER BY success_rate DESC
"""
# Commented out complex query; can explore by name instead if needed

# Close connection
con.close()
