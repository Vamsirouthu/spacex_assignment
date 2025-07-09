import pandas as pd
import folium
from folium.plugins import MarkerCluster

# Load cleaned dataset
df = pd.read_csv("spacex_full_data.csv")

# Drop rows without coordinates
df = df.dropna(subset=['latitude', 'longitude'])

# Create base map (centered on USA-ish area)
m = folium.Map(location=[28.5, -80.6], zoom_start=4)

# Marker cluster for better visuals
marker_cluster = MarkerCluster().add_to(m)

# Add markers to the map
for _, row in df.iterrows():
    location = [row['latitude'], row['longitude']]
    status = "Success " if row['landing_success'] == 1 else "Failure "
    popup_info = f"""
    <strong>Flight:</strong> {row['flight_number']}<br>
    <strong>Year:</strong> {row['launch_year']}<br>
    <strong>Site:</strong> {row['launch_site']}<br>
    <strong>Status:</strong> {status}
    """
    color = 'green' if row['landing_success'] == 1 else 'red'
    
    folium.Marker(
        location,
        popup=folium.Popup(popup_info, max_width=250),
        icon=folium.Icon(color=color)
    ).add_to(marker_cluster)

# Save to HTML
m.save("spacex_launch_map.html")
print("Map saved to spacex_launch_map.html")
