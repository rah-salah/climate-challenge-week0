# Dashboard Scripts

This folder is reserved for utility scripts related to the
African Climate Dashboard.

## Usage

The main dashboard application is located in the `app/` folder.

To run the dashboard locally:

1. Make sure your virtual environment is active:

```bash
   source .venv/Scripts/activate
```

2. Install streamlit if not already installed:

```bash
   pip install streamlit
```

3. Run the app from the project root folder:

```bash
   streamlit run app/main.py
```

4. Open your browser at:http://localhost:8501

## Notes

- The app reads data from the `data/` folder
- Make sure all cleaned CSV files are present in `data/`
- The `data/` folder is excluded from GitHub via `.gitignore`
