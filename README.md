# SpaceX Falcon 9 First Stage Landing Prediction

This project aims to predict whether the **first stage of the SpaceX Falcon 9 rocket** will successfully land after launch. By leveraging SpaceX's open API, Wikipedia launch records, and machine learning, we explore launch factors and build a binary classifier.

---

## Project Structure

```
spacex_assignment/
│
├── assignment1_api.py             # Data collection from SpaceX API
├── assignment2_scrape.py          # Web scraping Falcon 9 launch data from Wikipedia
├── assignment3_wrangle.py         # Data wrangling and preprocessing
├── assignment4_sql_eda.py         # SQL-based exploratory data analysis using DuckDB
├── assignment5_visual_eda.py      # Matplotlib/Seaborn visualizations
├── assignment6_folium_map.py      # Interactive map using Folium
├── assignment7_dash_dashboard.py  # Interactive dashboard with Plotly Dash
├── assignment8_modeling.py        # Classification models for landing prediction
│
├── spacex_full_data.csv           # Cleaned SpaceX API data
├── spacex_wiki_launch_data.csv    # Raw launch data scraped from Wikipedia
├── spacex_cleaned.csv             # Final preprocessed data for modeling
├── spacex_launch_map.html         # Folium-based interactive map
```

---

## Objectives

- Explore how payload, launch site, reuse history, and orbit type affect landing success
- Perform visual and SQL-based exploratory analysis
- Map global launch activity with success/failure markers
- Build and evaluate machine learning models to predict landings

---

## Technologies Used

- **Python 3.13**
- **Pandas, NumPy, Scikit-learn**
- **Matplotlib, Seaborn, Plotly Dash**
- **Folium, DuckDB**
- **BeautifulSoup & requests (for scraping)**
- **Jupyter + VS Code (optional)**

---

## Modeling Summary (Assignment 8)

| Model               | Accuracy | F1 Score | ROC AUC | Notes                           |
|--------------------|----------|----------|---------|----------------------------------|
| Logistic Regression| 74%      | 0.85     | 0.56    | Captures both classes using `class_weight=balanced` |
| Random Forest       | 90%      | 0.95     | 0.50    | High accuracy but biased toward class 1 (success) |

---

## Dashboard Preview (Assignment 7)

The interactive dashboard built using Dash includes:
- Launch site dropdown filter
- Payload mass slider
- Success rate pie chart
- Payload vs success scatter plot

Run locally with:
```bash
python assignment7_dash_dashboard.py
```

Then visit [http://127.0.0.1:8050](http://127.0.0.1:8050)

---

## Map Preview (Assignment 6)

Launch outcomes are visualized using Folium:
- Green markers: successful landings
- Red markers: failures

Open:
```
spacex_launch_map.html
```

---

## Setup Instructions

1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/spacex-assignment.git
   cd spacex-assignment
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run any module:
   ```bash
   python assignment1_api.py
   ```

---

## Author

**Vamsi Routhu**  
Graduate Student, DePaul University  
Data Science & Machine Learning Enthusiast

---

## License

This project is for academic purposes and learning. No affiliation with SpaceX.
