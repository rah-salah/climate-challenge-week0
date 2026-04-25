import pandas as pd
import numpy as np
from scipy import stats
import os
import streamlit as st

COUNTRIES = ["Ethiopia", "Kenya", "Sudan", "Tanzania", "Nigeria"]

COLORS = {
    "Ethiopia": "#636EFA",
    "Kenya": "#EF553B",
    "Sudan": "#00CC96",
    "Tanzania": "#AB63FA",
    "Nigeria": "#FFA15A"
}

@st.cache_data
def load_data(countries, sample_only=False, sample_rows=10000):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    data_dir = os.path.join(project_root, "data")
    sample_dir = os.path.join(project_root, "sample_data")

    frames = []
    for country in countries:
        path = os.path.join(data_dir, f"{country.lower()}_clean.csv")
        sample_path = os.path.join(sample_dir, f"{country.lower()}_clean.csv")

        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["Date"])
            frames.append(df)
        elif os.path.exists(sample_path):
            df = pd.read_csv(sample_path, parse_dates=["Date"])
            frames.append(df)
        else:
            st.warning(f"No data found for {country}")

    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

def filter_by_year(df, start_year, end_year):
    return df[(df["YEAR"] >= start_year) & (df["YEAR"] <= end_year)]

def get_monthly_avg(df, variable):
    monthly = df.groupby(["Country", "YEAR", "Month"])[variable].mean().reset_index()
    monthly["Date"] = pd.to_datetime(monthly[["YEAR", "Month"]].assign(DAY=1))
    return monthly

def summary_table(df, variable):
    return df.groupby("Country")[variable].agg(
        Mean="mean", Median="median", Std="std", Max="max"
    ).round(2)

def run_kruskal(df, variable):
    if df.empty:
        return {"stat": 0, "p_value": 1.0}
    groups = [
        df[df["Country"] == c][variable].dropna().values
        for c in df["Country"].unique()
    ]
    if len(groups) < 2:
        return {"stat": 0, "p_value": 1.0}
    stat, p_value = stats.kruskal(*groups)
    return {"stat": round(stat, 4), "p_value": p_value}

def vulnerability_ranking(df):
    heat_days = df[df["T2M_MAX"] > 35].groupby("Country").size()
    dry_days = df[df["PRECTOTCORR"] < 1].groupby("Country").size()
    mean_temp = df.groupby("Country")["T2M"].mean().round(2)
    mean_rain = df.groupby("Country")["PRECTOTCORR"].mean().round(2)

    ranking = pd.DataFrame({
        "Mean Temp (°C)": mean_temp,
        "Mean Rainfall (mm)": mean_rain,
        "Extreme Heat Days": heat_days,
        "Dry Days": dry_days
    }).fillna(0).astype({"Extreme Heat Days": int, "Dry Days": int})

    return ranking.sort_values("Mean Temp (°C)", ascending=False)