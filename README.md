# Chicago 911 Response Time Inequality Tracker
An interactive web dashboard analyzing emergency response time disparities across Chicago neighborhoods,
with a focus on the relationship between neighborhood income and 911 response times.

**[Live App](https://chicago911-tracker.streamlit.app/)**

## What Project Does
Residents in lower income Chicago neighborhoods wait longer for emergency serivces. This dashboard makes
that inequality visible and explorable.

-Compares median 911 response times across 40+ Chicago neighborhoods.
-Tests the correlation between neighborhood median household income and response time.
- Interactive filters by incident type(Medical / Fire/ Police) and year range.
- Color-coded Folium map with neighborhood level response time markers
- Neighborhood lookup tool for individual community area stats

## Key Finding
Statistically significant negative correlation between beighborhood median household income and 911 
response times. Lower income areas experience meaningfully slower emergency response.

## Teach Stack

| Layer | Tools |
| ----- | ----- |
| App framework | Streamlit |
| Data Processing | Python, Pandas |
| Visualization | Plotly , Folium |
| Deployment | Streamlit Community Cloud |

## Project Structure
chicago911-tracker/
|---- app.py              # Main Streamlit application
|---- utlis/
|  |----data_loader.py    # Data ingestion and preprocessing
|  |----analysis.py       # Statistical analysis functions
|---- data/               # Dataset files
|----requirements.txt     # Dependencies 

## Run Locally
```bash
git clone https://github.com/MahiPatel23/chicago911-tracker.git
cd chicago911-tracker
pip install -r requirements.txt
streamlit run app.py
```


## Author
**Mahi Patel**  - Data Science student at University of Illinois Chicago
[LinedIn](https://www.linkedin.com/in/mahi-patel-5750492a0/) 
[Github](https://github.com/MahiPatel23)
