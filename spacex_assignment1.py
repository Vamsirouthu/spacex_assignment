import requests
import pandas as pd
from datetime import datetime
from tqdm import tqdm

# API endpoints
launches_url = "https://api.spacexdata.com/v4/launches"
rockets_url = "https://api.spacexdata.com/v4/rockets/"
payloads_url = "https://api.spacexdata.com/v4/payloads/"
launchpads_url = "https://api.spacexdata.com/v4/launchpads/"
landpads_url = "https://api.spacexdata.com/v4/landpads/"

# Load launches
launches = requests.get(launches_url).json()

data = []

for launch in tqdm(launches):
    try:
        flight_number = launch.get('flight_number')
        date_utc = launch.get('date_utc')
        launch_year = datetime.strptime(date_utc, "%Y-%m-%dT%H:%M:%S.%fZ").year if date_utc else None

        rocket_id = launch.get('rocket')
        launchpad_id = launch.get('launchpad')
        payload_ids = launch.get('payloads', [])
        cores = launch.get('cores', [])

        if not (rocket_id and launchpad_id and cores):
            continue

        # Rocket info
        rocket_data = requests.get(rockets_url + rocket_id).json()
        rocket_name = rocket_data.get('name')
        booster_version = rocket_data.get('description', 'NaN')[:50]

        # Launchpad info
        launchpad_data = requests.get(launchpads_url + launchpad_id).json()
        launch_site = launchpad_data.get('name')
        latitude = launchpad_data.get('latitude')
        longitude = launchpad_data.get('longitude')

        # Payload info
        payload_mass_total = 0
        orbits = []
        for payload_id in payload_ids:
            payload = requests.get(payloads_url + payload_id).json()
            mass = payload.get('mass_kg', 0)
            orbit = payload.get('orbit', 'NaN')
            if mass:
                payload_mass_total += mass
            if orbit:
                orbits.append(orbit)
        orbit_combined = ','.join(list(set(orbits))) if orbits else 'NaN'


        # Core info
        core_info = cores[0] if cores else {}
        landing_success = core_info.get('landing_success')
        reused = core_info.get('reused')
        landing_type = core_info.get('landing_type')
        landpad_id = core_info.get('landpad')
        landpad_name = 'NaN'

        if landpad_id:
            landpad = requests.get(landpads_url + landpad_id).json()
            landpad_name = landpad.get('full_name', 'NaN')

        data.append({
            'flight_number': flight_number,
            'date_utc': date_utc,
            'launch_year': launch_year,
            'rocket_name': rocket_name,
            'booster_version': booster_version,
            'launch_site': launch_site,
            'latitude': latitude,
            'longitude': longitude,
            'payload_mass_kg': payload_mass_total,
            'orbit': orbit_combined,
            'landing_success': landing_success,
            'landing_type': landing_type,
            'landpad_name': landpad_name,
            'reused': reused,
            'number_of_cores': len(cores),
            'number_of_payloads': len(payload_ids)
        })

    except Exception as e:
        print(f"Error in launch {launch.get('name')}: {e}")
        continue

# Save to DataFrame
df = pd.DataFrame(data)
df.to_csv("spacex_full_data.csv", index=False)
print("Data saved to spacex_full_data.csv")
