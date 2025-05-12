# Data Analysis Dashboard

This is a Streamlit-based data analysis dashboard that allows users to upload CSV files, visualize data, and perform basic analysis.

## Features

- CSV file upload and data cleaning
- Interactive data filtering
- Multiple visualization types (Line, Bar, Pie charts, and Heatmap)
- Data download options (CSV/Excel)
- Raw data display

## Local Deployment

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Create a GitHub repository and push your code:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your repository, branch, and main file (app.py)
6. Click "Deploy"

## Project Structure

- `app.py`: Main Streamlit application
- `utils.py`: Utility functions for data processing and visualization
- `requirements.txt`: Project dependencies

## Usage

1. Upload a CSV file using the file uploader
2. Use the sidebar filters to filter your data
3. Select visualization type and customize the chart
4. Download the filtered data in CSV or Excel format