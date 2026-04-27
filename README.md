# 🌍 African Climate Data Analysis — COP32 Week 0

## Live Dashboard
👉 https://climate-challenge-week0-g98shd72clsx6pwpmoxzvf.streamlit.app/

## Project Overview
This project analyzes daily climate data from NASA POWER satellite measurements across five African countries — Ethiopia, Kenya, Sudan, Tanzania, and Nigeria — covering January 2015 to March 2026.

It was completed as part of 10 Academy KAIM 9 Week 0 Challenge. The goal is to extract climate insights to support Ethiopia's position at COP32 in 2027.

## Repository Structure
notebooks/
├── ethiopia_eda.ipynb       # EDA for Ethiopia
├── kenya_eda.ipynb          # EDA for Kenya
├── sudan_eda.ipynb          # EDA for Sudan
├── tanzania_eda.ipynb       # EDA for Tanzania
├── nigeria_eda.ipynb        # EDA for Nigeria
└── compare_countries.ipynb  # Cross-country comparison and COP32 insights
app/
├── main.py                  # Streamlit dashboard
└── utils.py                 # Data processing utilities
data/                        # NASA CSV files — excluded from GitHub via .gitignore
sample_data/                 # Sample data for Streamlit Cloud deployment
tests/                       # CI test files
.github/workflows/ci.yml     # GitHub Actions CI pipeline
requirements.txt             # Python dependencies

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/rah-salah/climate-challenge-week0.git
cd climate-challenge-week0
```

### 2. Create and activate virtual environment
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows
source .venv/bin/activate       # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add data files
Place the NASA POWER CSV files in a data/ folder:
data/
├── Ethiopia.csv
├── Kenya.csv
├── Sudan.csv
├── Tanzania.csv
└── Nigeria.csv

### 5. Launch Jupyter
```bash
jupyter notebook
```

## Each Country Notebook Contains
- Data loading and date parsing
- Missing value and duplicate handling
- Summary statistics with written interpretation
- Outlier detection using Z-scores
- Forward-fill for remaining missing values
- Temperature trend line chart with annotations
- Rainfall bar chart with peak month annotated
- Correlation heatmap and scatter plots
- Rainfall histogram and bubble chart
- Written markdown interpretation for every plot

## Running the Dashboard
```bash
streamlit run app/main.py
```
Open your browser at http://localhost:8501

## Key Findings
- Sudan is the most vulnerable country — mean temp 28.76°C, 2694 extreme heat days, 3696 dry days
- All 5 countries show a warming trend from 2015 to 2026
- Kruskal-Wallis test confirms differences are statistically significant (p ≈ 0)
- Nigeria has the highest single-day rainfall of 166.10mm
- Ethiopia and Kenya combined have nearly 5000 dry days

## CI Pipeline
GitHub Actions automatically installs dependencies and runs pytest on every push.
