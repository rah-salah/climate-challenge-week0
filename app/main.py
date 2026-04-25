import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
import os

curr_dir = os.path.dirname(os.path.abspath(__file__))
if curr_dir not in sys.path:
    sys.path.insert(0, curr_dir)

from utils import (
    COUNTRIES, COLORS, load_data, filter_by_year,
    get_monthly_avg, summary_table, run_kruskal, vulnerability_ranking
)

# ── PAGE CONFIG ────────────────────────────────────────
st.set_page_config(
    page_title="African Climate Dashboard | COP32",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ─────────────────────────────────────────
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent !important;
        border-radius: 4px 4px 0px 0px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 2px solid #007bff !important;
        color: #007bff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────
col_title, col_space = st.columns([4, 1])
with col_title:
    st.title("🌍 African Climate Dashboard — COP32 Analysis")
    st.markdown(
        "Explore and compare climate trends across **5 African countries** "
        "from 2015 to 2026. Built for Ethiopia's COP32 position paper."
    )
st.divider()

# ── SIDEBAR ────────────────────────────────────────────
with st.sidebar:
    st.header("Dashboard Controls")

    st.subheader("Country Selection")
    selected_countries = st.multiselect(
        "Select Countries",
        options=COUNTRIES,
        default=COUNTRIES
    )

    st.subheader("Year Range")
    year_range = st.slider(
        "Select Period",
        min_value=2015,
        max_value=2026,
        value=(2015, 2026)
    )

    st.subheader("Climate Variable")
    variable = st.selectbox(
        "Select Variable",
        options=["T2M", "T2M_MAX", "T2M_MIN", "PRECTOTCORR", "RH2M", "WS2M"],
        format_func=lambda x: {
            "T2M": "Mean Temperature (°C)",
            "T2M_MAX": "Max Temperature (°C)",
            "T2M_MIN": "Min Temperature (°C)",
            "PRECTOTCORR": "Rainfall (mm)",
            "RH2M": "Relative Humidity (%)",
            "WS2M": "Wind Speed (m/s)"
        }[x]
    )

    full_load = st.checkbox("Load full dataset", value=False)
    st.divider()
    st.caption("Data: NASA POWER Satellite\n10 Academy KAIM 9 — Week 0")

# ── GUARD ──────────────────────────────────────────────
if not selected_countries:
    st.error("Please select at least one country.")
    st.stop()

# ── LOAD DATA ──────────────────────────────────────────
with st.spinner("Loading climate data..."):
    try:
        df_raw = load_data(selected_countries, sample_only=False)
        if df_raw.empty:
            st.error("No data found. Make sure cleaned CSV files are in the data/ folder.")
            st.stop()
        df = filter_by_year(df_raw, year_range[0], year_range[1])
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

# ── KPI METRICS ────────────────────────────────────────
st.subheader("📊 Key Climate Indicators")
kpi_cols = st.columns(len(selected_countries))
for i, country in enumerate(selected_countries):
    cdf = df[df["Country"] == country]
    if not cdf.empty:
        kpi_cols[i].metric(
            label=country,
            value=f"{cdf['T2M'].mean():.1f}°C",
            delta=f"Max: {cdf['T2M_MAX'].max():.1f}°C"
        )

st.divider()

# ── TABS ───────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Time Series",
    "📦 Distribution",
    "📋 Summary & Stats",
    "🏆 Vulnerability Ranking"
])

# ── TAB 1: TIME SERIES ─────────────────────────────────
with tab1:
    st.markdown(f"### Monthly Average {variable} Trend")
    monthly = get_monthly_avg(df, variable)

    fig_line = px.line(
        monthly,
        x="Date",
        y=variable,
        color="Country",
        color_discrete_map=COLORS,
        template="plotly_white",
        labels={"Date": "Year", variable: variable}
    )
    fig_line.update_layout(
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.markdown(f"### Monthly Total Rainfall Trend")
    monthly_rain = get_monthly_avg(df, "PRECTOTCORR")
    fig_rain = px.bar(
        monthly_rain,
        x="Date",
        y="PRECTOTCORR",
        color="Country",
        color_discrete_map=COLORS,
        template="plotly_white",
        barmode="group",
        labels={"Date": "Year", "PRECTOTCORR": "Rainfall (mm)"}
    )
    st.plotly_chart(fig_rain, use_container_width=True)

# ── TAB 2: DISTRIBUTION ────────────────────────────────
with tab2:
    st.markdown(f"### {variable} Distribution by Country")
    col_box, col_hist = st.columns(2)

    with col_box:
        fig_box = px.box(
            df,
            x="Country",
            y=variable,
            color="Country",
            color_discrete_map=COLORS,
            template="plotly_white",
            points=False,
            title="Boxplot"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_hist:
        fig_hist = px.histogram(
            df,
            x=variable,
            color="Country",
            barmode="overlay",
            color_discrete_map=COLORS,
            template="plotly_white",
            nbins=50,
            title="Histogram"
        )
        st.plotly_chart(fig_hist, use_container_width=True)

# ── TAB 3: SUMMARY & STATS ─────────────────────────────
with tab3:
    st.markdown("### Summary Statistics")
    stats_df = summary_table(df, variable)
    st.dataframe(stats_df, use_container_width=True)

    st.divider()
    col_test, col_info = st.columns([1, 1])

    with col_test:
        st.markdown(f"### Kruskal-Wallis Test ({variable})")
        result = run_kruskal(df, variable)
        c1, c2 = st.columns(2)
        c1.metric("Test Statistic", result["stat"])
        c2.metric("P-value", f"{result['p_value']:.4e}")

        if result["p_value"] < 0.05:
            st.success("Differences between countries are statistically significant.")
        else:
            st.warning("No statistically significant difference found.")

    with col_info:
        st.info("""
        **About the Kruskal-Wallis Test**
        - A non-parametric test comparing climate variables across all 5 countries
        - P-value < 0.05 means the differences are real and not due to chance
        - Used to confirm that climate conditions differ significantly across Africa
        """)

# ── TAB 4: VULNERABILITY RANKING ──────────────────────
with tab4:
    st.markdown("### Climate Vulnerability Ranking")
    st.markdown("Countries ranked by mean temperature, extreme heat days and dry days.")

    ranking = vulnerability_ranking(df)
    st.dataframe(ranking, use_container_width=True)

    st.divider()
    fig_rank = px.bar(
        ranking.reset_index(),
        x="Country",
        y="Mean Temp (°C)",
        color="Country",
        color_discrete_map=COLORS,
        template="plotly_white",
        text_auto=".1f",
        title="Mean Temperature by Country (Higher = More Heat Stress)"
    )
    fig_rank.update_traces(textposition="outside")
    st.plotly_chart(fig_rank, use_container_width=True)

    st.markdown("""
    ### COP32 Key Findings
    1. **Sudan** is the most climate-vulnerable country with the highest temperatures and most dry days
    2. **Kenya** faces serious drought risk with 2,831 dry days over 11 years
    3. **Nigeria and Tanzania** face growing flood risk from extreme rainfall events
    4. **All 5 countries** show a consistent warming trend from 2015 to 2026
    5. **Ethiopia** should champion Sudan for priority climate finance at COP32
    """)

# ── FOOTER ─────────────────────────────────────────────
st.divider()
st.caption("Built with Streamlit · NASA POWER Data · 10 Academy KAIM 9 · Rahma Salah")