import streamlit as st
from utils.data_loader import load911_data, load_census_data
from utils.analysis import compute_neighborhood_stats, comp_income_corr
import plotly.express as px
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Chicago 911 Tracker", page_icon="🚨", layout="wide")

st.title("🚨 Chicago 911 Response Time Tracker")
st.caption("Analyzing emergency response equity across Chicago neighborhoods")

# ── Sidebar ──────────────────────────────────────────────────────
st.sidebar.title("Filters")

incident_type = st.sidebar.selectbox(
    "Incident type",
    ["All", "Medical", "Fire", "Police"]
)

year_range = st.sidebar.slider(
    "Year range",
    min_value=2019, max_value=2024, value=(2021, 2023)
)

top_n = st.sidebar.slider("Top N neighborhoods", 5, 20, 12)

# ── Load data ─────────────────────────────────────────────────────
df = load911_data()
census = load_census_data()

# ── Filter ────────────────────────────────────────────────────────
df = df[df["year"].between(year_range[0], year_range[1])]
if incident_type != "All":
    df = df[df["incident_type"] == incident_type]

# ── KPIs ──────────────────────────────────────────────────────────
st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Median response time", f"{df['response_min'].median():.1f} min")
col2.metric("Total incidents", f"{len(df):,}")
col3.metric("Neighborhoods tracked", df["neighborhood"].nunique())

st.markdown("---")

# ── Chart 1: Response by neighborhood ────────────────────────────
st.subheader("Response time by neighborhood")
stats = compute_neighborhood_stats(df, top_n)
fig = px.bar(
    stats,
    x="median_response_min",
    y="neighborhood",
    orientation="h",
    color="median_response_min",
    color_continuous_scale=["#2dc653", "#f6c90e", "#e63946"],
    labels={"median_response_min": "Median response time (min)", "neighborhood": ""},
)
fig.update_layout(coloraxis_showscale=False, plot_bgcolor="white",
                  yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig, use_container_width=True)

# ── Chart 2: Income correlation ───────────────────────────────────
st.subheader("Does income predict response time?")
corr_df = comp_income_corr(df, census)
fig2 = px.scatter(
    corr_df,
    x="median_household_income",
    y="median_response_min",
    text="neighborhood",
    labels={
        "median_household_income": "Median household income ($)",
        "median_response_min": "Median response time (min)"
    }
)
fig2.update_layout(plot_bgcolor="white")
st.plotly_chart(fig2, use_container_width=True)

# ── Neighborhood lookup ───────────────────────────────────────────
st.markdown("---")
st.subheader("Look up your neighborhood")
selected = st.selectbox("Select a neighborhood", sorted(df["neighborhood"].unique()))
nb_df = df[df["neighborhood"] == selected]
c1, c2 = st.columns(2)
c1.metric("Median response time", f"{nb_df['response_min'].median():.1f} min")
c2.metric("Total incidents", f"{len(nb_df):,}")

# ── Map ───────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("Response time map")

neighborhood_coords = {
    "Rogers Park": [42.0083, -87.6648],
    "West Ridge": [41.9986, -87.6817],
    "Uptown": [41.9784, -87.6543],
    "Lincoln Square": [41.9681, -87.6753],
    "Lake View": [41.9434, -87.6431],
    "Lincoln Park": [41.9241, -87.6488],
    "Near North Side": [41.9001, -87.6341],
    "Edison Park": [41.9856, -87.8133],
    "Jefferson Park": [41.9706, -87.7614],
    "Albany Park": [41.9681, -87.7243],
    "Portage Park": [41.9372, -87.7614],
    "Irving Park": [41.9536, -87.7243],
    "Logan Square": [41.9217, -87.7034],
    "Humboldt Park": [41.8994, -87.7243],
    "West Town": [41.8951, -87.6681],
    "Austin": [41.8948, -87.7648],
    "West Garfield Park": [41.8794, -87.7414],
    "North Lawndale": [41.8594, -87.7243],
    "Near West Side": [41.8748, -87.6681],
    "Loop": [41.8827, -87.6278],
    "Near South Side": [41.8594, -87.6278],
    "Douglas": [41.8394, -87.6148],
    "Grand Boulevard": [41.8194, -87.6148],
    "Kenwood": [41.8094, -87.5948],
    "Washington Park": [41.7894, -87.6148],
    "Hyde Park": [41.7994, -87.5848],
    "Woodlawn": [41.7794, -87.5948],
    "South Shore": [41.7594, -87.5748],
    "Chatham": [41.7494, -87.6148],
    "Roseland": [41.7094, -87.6248],
    "Pullman": [41.7094, -87.6048],
    "West Pullman": [41.6894, -87.6448],
    "Riverdale": [41.6494, -87.6248],
    "Englewood": [41.7794, -87.6448],
    "West Englewood": [41.7794, -87.6648],
    "Greater Grand Crossing": [41.7594, -87.6148],
    "Auburn Gresham": [41.7394, -87.6448],
    "Beverly": [41.7194, -87.6648],
    "Washington Heights": [41.7094, -87.6548],
    "Mount Greenwood": [41.6994, -87.6948],
    "Morgan Park": [41.6894, -87.6648],
}

m = folium.Map(location=[41.85, -87.65], zoom_start=11, tiles="CartoDB positron")

nb_stats = df.groupby("neighborhood")["response_min"].median()

for nb, coords in neighborhood_coords.items():
    if nb in nb_stats:
        response = nb_stats[nb]
        if response < 7:
            color = "green"
        elif response < 10:
            color = "orange"
        else:
            color = "red"

        folium.CircleMarker(
            location=coords,
            radius=10,
            color=color,
            fill=True,
            fill_opacity=0.7,
            tooltip=f"{nb}: {response:.1f} min"
        ).add_to(m)

st_folium(m, width=700, height=500)
st.caption("🟢 Fast (< 7 min)  🟠 Medium (7–10 min)  🔴 Slow (> 10 min) — hover over circles for details")