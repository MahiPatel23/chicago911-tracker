import pandas as pd
import numpy as np

def compute_neighborhood_stats(df, top_n = 15):
    stats = (
        df.groupby("neighborhood")["response_min"]
        .agg(median_response_min = "median", count = "count")
        .reset_index()
        .sort_values("median_response_min", ascending = False)
        .head(top_n)
    )
    return stats

def comp_income_corr(df, census):
    stats = (
        df.groupby("neighborhood")["response_min"]
        .median()
        .reset_index()
        .rename(columns={"response_min": "median_response_min"})
    )
    merged = stats.merge(census, on="neighborhood", how = "inner")
    return merged