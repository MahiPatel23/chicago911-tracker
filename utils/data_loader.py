import pandas as pd
import numpy as np
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

NEIGHBORHOODS = [
    "Rogers Park","West Ridge","Uptown","Lincoln Square",
    "Lake View","Lincoln Park","Near North Side","Edison Park",
    "Jefferson Park","Albany Park","Portage Park","Irving Park",
    "Logan Square", "Humboldt Park", "West Town", "Austin",
    "West Garfield Park", "North Lawndale", "Near West Side",
    "Loop", "Near South Side", "Douglas", "Grand Boulevard",
    "Kenwood", "Washington Park", "Hyde Park", "Woodlawn",
    "South Shore", "Chatham", "Roseland", "Pullman",
    "West Pullman", "Riverdale", "Englewood", "West Englewood",
    "Greater Grand Crossing", "Auburn Gresham", "Beverly",
    "Washington Heights", "Mount Greenwood", "Morgan Park",
]

INCOME_MAP = {
    "Lincoln Park": 112000, "Lake View": 98000, "Near North Side": 105000,
    "Loop": 89000, "Hyde Park": 72000, "Rogers Park": 41000,
    "Englewood": 22000, "West Garfield Park": 24000, "North Lawndale": 26000,
    "Roseland": 34000, "Auburn Gresham": 36000, "Austin": 31000,
    "Humboldt Park": 30000, "South Shore": 33000, "Woodlawn": 29000,
    "West Englewood": 25000, "Riverdale": 17000,
    "Greater Grand Crossing": 32000, "Chatham": 40000,
    "Beverly": 78000, "Mount Greenwood": 74000, "Edison Park": 81000,
}

def synthetic_data():
    np.random.seed(42)
    n = 15000
    neighborhoods = np.random.choice(NEIGHBORHOODS, size = n)
    response_base = []
    for nb in neighborhoods:
        income = INCOME_MAP.get(nb, 50000)
        base = 6 + (80000 - income) / 80000 * 6
        response_base.append(max(2,base +np.random.normal(0,2)))

    years = np.random.choice(range(2019, 2025), size = n)
    months = np.random.randint(1, 13, size = n)
    incident_types = np.random.choice(
        ["Medical","Fire","Police"],size = n, p = [0.45,0.15,0.40]
    )

    response_min = np.array(response_base)
    response_min[incident_types == "Medical"] *= 0.85
    response_min[incident_types == "Fire"] *= 0.90
    response_min += np.random.exponential(1.5,size = n)
    response_min = np.clip(response_min, 1, 45)

    data = pd.DataFrame({
        "neighborhood" : neighborhoods,
        "year" : years,
        "month" : months,
        "incident_type" : incident_types,
        "response_min" : np.round(response_min, 2),
    })
    return data

def load911_data():
    path_file = DATA_DIR/"911_calls.csv"
    if path_file.exists():
        return pd.read_csv(path_file)
    data = synthetic_data()
    DATA_DIR.mkdir(exist_ok = True)
    data.to_csv(path_file, index = False)
    return data

def load_census_data():
    rows = [
        {"neighborhood" : nb, "median_household_income" : inc}
        for nb, inc in INCOME_MAP.items()
    ]
    return pd.DataFrame(rows)