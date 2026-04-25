## Interactive Dashboard

An interactive Streamlit dashboard is available to explore the climate data visually.

### Running Locally

1. Activate your virtual environment:

```bash
   source .venv/Scripts/activate
```

2. Install dependencies:

```bash
   pip install -r requirements.txt
```

3. Run the dashboard:

```bash
   streamlit run app/main.py
```

4. Open your browser at:http://localhost:8501

### Dashboard Features

- Country multi-select to filter by country
- Year range slider to zoom into specific periods
- Variable selector dropdown (T2M, PRECTOTCORR, RH2M, etc.)
- Temperature trend line chart
- Rainfall distribution boxplot
- Summary statistics table
- Climate vulnerability ranking
- Kruskal-Wallis statistical test results

### Note on Data

The dashboard reads from `data/<country>_clean.csv` files locally.
On Streamlit Cloud it uses sample data from `sample_data/` folder.
