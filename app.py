import streamlit as st
import pandas as pd
import json
import os
from pathlib import Path
import hashlib
from utils import (
    clean_data,
    compare_datasets,
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_heatmap,
    get_download_link,
    apply_filters
)

# Set page config at the very beginning
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# --- THEME MANAGEMENT ---
def set_theme():
    theme = st.session_state.get('theme', 'dark')
    if theme == 'dark':
        st.markdown('''<style>
        body, .stApp { background-color: #18191A !important; color: #F5F6F7 !important; }
        .big-card {background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: #F5F6F7; border-radius: 16px; padding: 32px 0; margin: 8px; box-shadow: 0 2px 8px #0003; text-align: center; font-size: 2rem; border: 2px solid #4F8BF9;}
        .stButton>button {background: #2563eb; color: #fff; border-radius: 8px; border: 1px solid #4F8BF9;}
        .stRadio>div {color: #F5F6F7;}
        .stDataFrame, .stTable {background: #23272F !important; color: #F5F6F7 !important;}
        </style>''', unsafe_allow_html=True)
    else:
        st.markdown('''<style>
        body, .stApp { background-color: #f8fafc !important; color: #18191A !important; }
        .big-card {background: #fff; color: #18191A; border-radius: 16px; padding: 32px 0; margin: 8px; box-shadow: 0 2px 8px #0001; text-align: center; font-size: 2rem; border: 2px solid #4F8BF9;}
        .stButton>button {background: #4F8BF9; color: #fff; border-radius: 8px; border: 1px solid #2563eb;}
        .stRadio>div {color: #18191A;}
        .stDataFrame, .stTable {background: #fff !important; color: #18191A !important;}
        </style>''', unsafe_allow_html=True)

# --- SESSION STATE INIT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = 'Home'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'show_default' not in st.session_state:
    st.session_state.show_default = True

set_theme()

# --- AUTH ---
USER_DATA_FILE = Path("data/users/users.json")
def load_users():
    if USER_DATA_FILE.exists():
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}
def save_users(users):
    USER_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_page():
    st.title("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        if submit:
            users = load_users()
            if username in users and users[username]['password'] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.experimental_rerun()
            else:
                st.error("Invalid username or password")

def signup_page():
    st.title("Sign Up")
    with st.form("signup_form"):
        new_username = st.text_input("Choose Username")
        new_password = st.text_input("Choose Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Sign Up")
        if submit:
            if new_password != confirm_password:
                st.error("Passwords do not match!")
                return
            users = load_users()
            if new_username in users:
                st.error("Username already exists!")
                return
            users[new_username] = {'password': hash_password(new_password)}
            save_users(users)
            st.success("Sign up successful! Please login.")
            st.session_state.show_login = True
            st.experimental_rerun()

# --- SIDEBAR NAVIGATION ---
def sidebar():
    st.sidebar.title("KUBER INDUSTRY")
    st.sidebar.markdown("---")
    page = st.sidebar.radio("Navigation", ["Home", "Static Data", "Dynamic Comparison", "Settings"], index=["Home", "Static Data", "Dynamic Comparison", "Settings"].index(st.session_state.page))
    st.session_state.page = page
    st.sidebar.markdown(f"Logged in as: {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.page = 'Home'
        st.experimental_rerun()

# --- BIG SUMMARY CARDS ---
def big_summary_cards(df):
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) == 0:
        st.info("No numeric columns for summary.")
        return
    sum_val = df[numeric_cols].sum().sum()
    count_val = len(df)
    max_val = df[numeric_cols].max().max()
    min_val = df[numeric_cols].min().min()
    card_titles = ["Sum", "Count", "Max", "Min"]
    card_values = [f"{sum_val:,.2f}", f"{count_val}", f"{max_val:,.2f}", f"{min_val:,.2f}"]
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            st.markdown(f'<div class="big-card">{card_titles[i]}<br><b>{card_values[i]}</b></div>', unsafe_allow_html=True)

# --- ADVANCED FEATURES ---
def quick_filter(df):
    search = st.text_input("Quick Filter (search in all columns)")
    if search:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
    return df

def export_pdf_button():
    st.info("PDF export coming soon! (Demo placeholder)")
    st.button("Export as PDF")

def top_n_filter(df):
    numeric_cols = df.select_dtypes(include='number').columns
    if len(numeric_cols) == 0:
        return df
    col = st.selectbox("Top N by column", numeric_cols, key="topn")
    n = st.slider("N", 5, 50, 10)
    return df.nlargest(n, col)

# --- TIME FILTER ---
def time_filter(df):
    date_cols = df.select_dtypes(include=['datetime', 'object']).columns
    date_col = None
    for col in date_cols:
        try:
            pd.to_datetime(df[col])
            date_col = col
            break
        except:
            continue
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        min_date, max_date = df[date_col].min(), df[date_col].max()
        date_range = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
        df = df[(df[date_col] >= date_range[0]) & (df[date_col] <= date_range[1])]
    return df

# --- MULTI-CHARTS ---
def multi_charts(df, prefix=""):
    chart_types = ["Line Chart", "Bar Chart", "Pie Chart", "Heatmap", "Correlation Matrix"]
    chart_count = st.number_input(f"How many charts to show?", 1, 5, 1, key=f"{prefix}chartcount")
    for i in range(chart_count):
        st.markdown(f"#### Chart {i+1}")
        chart_type = st.selectbox(f"Chart Type", chart_types, key=f"{prefix}charttype{i}")
        if chart_type == "Line Chart":
            x_col = st.selectbox("X-axis", df.columns, key=f"{prefix}x{i}")
            y_col = st.selectbox("Y-axis", df.select_dtypes(include='number').columns, key=f"{prefix}y{i}")
            fig = create_line_chart(df, x_col, y_col, f"{y_col} vs {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Bar Chart":
            x_col = st.selectbox("X-axis", df.columns, key=f"{prefix}bx{i}")
            y_col = st.selectbox("Y-axis", df.select_dtypes(include='number').columns, key=f"{prefix}by{i}")
            fig = create_bar_chart(df, x_col, y_col, f"{y_col} by {x_col}")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Pie Chart":
            values_col = st.selectbox("Values", df.select_dtypes(include='number').columns, key=f"{prefix}pv{i}")
            names_col = st.selectbox("Categories", df.columns, key=f"{prefix}pn{i}")
            fig = create_pie_chart(df, values_col, names_col, f"{values_col} by {names_col}")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Heatmap":
            fig = create_heatmap(df, "Correlation Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Correlation Matrix":
            corr = df.select_dtypes(include='number').corr()
            st.dataframe(corr)

# --- HOME PAGE ---
def home_page():
    st.header("Welcome to Kuber Industry Analytics")
    if st.session_state.show_default:
        try:
            df = pd.read_csv("Test.csv")
            st.subheader("Default Data Preview")
            big_summary_cards(df)
            st.markdown("#### Data Visualization")
            multi_charts(df, prefix="home")
            st.markdown("#### Data Table")
            df = quick_filter(df)
            st.dataframe(df.head(20))
            export_pdf_button()
            if st.button("Remove Default Data"):
                st.session_state.show_default = False
                st.experimental_rerun()
        except Exception as e:
            st.error(f"Error loading default data: {e}")
    else:
        st.info("Default data removed. Please use other options from the sidebar.")

# --- STATIC DATA PAGE ---
def static_data_page():
    st.header("Static Data Analysis")
    uploaded_file = st.file_uploader("Upload your CSV file", type="csv", key="static")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df = clean_data(df)
        st.subheader("Summary Cards")
        big_summary_cards(df)
        df = time_filter(df)
        st.markdown("#### Data Visualization")
        multi_charts(df, prefix="static")
        st.markdown("#### Data Table")
        df = quick_filter(df)
        df = top_n_filter(df)
        st.dataframe(df, use_container_width=True)
        export_pdf_button()

# --- DYNAMIC COMPARISON PAGE ---
def dynamic_comparison_page():
    st.header("Dynamic Data Comparison")
    uploaded_file1 = st.file_uploader("Upload first CSV file", type="csv", key="dynamic1")
    uploaded_file2 = st.file_uploader("Upload second CSV file", type="csv", key="dynamic2")
    if uploaded_file1 and uploaded_file2:
        df1 = pd.read_csv(uploaded_file1)
        df2 = pd.read_csv(uploaded_file2)
        df1 = clean_data(df1)
        df2 = clean_data(df2)
        st.subheader("Summary Cards - File 1")
        big_summary_cards(df1)
        st.subheader("Summary Cards - File 2")
        big_summary_cards(df2)
        df1 = time_filter(df1)
        df2 = time_filter(df2)
        st.markdown("#### Visualization - File 1")
        multi_charts(df1, prefix="dyn1")
        st.markdown("#### Visualization - File 2")
        multi_charts(df2, prefix="dyn2")
        st.markdown("#### Data Table - File 1")
        df1 = quick_filter(df1)
        df1 = top_n_filter(df1)
        st.dataframe(df1, use_container_width=True)
        st.markdown("#### Data Table - File 2")
        df2 = quick_filter(df2)
        df2 = top_n_filter(df2)
        st.dataframe(df2, use_container_width=True)
        export_pdf_button()

# --- SETTINGS PAGE ---
def settings_page():
    st.header("Settings")
    theme = st.radio("Select Theme", ["dark", "light"], index=["dark", "light"].index(st.session_state.theme))
    if theme != st.session_state.theme:
        st.session_state.theme = theme
        st.experimental_rerun()
    st.info("Default is dark blue. Switch to light only if you want a light look.")

# --- MAIN APP ---
def main_app():
    sidebar()
    if st.session_state.page == "Home":
        home_page()
    elif st.session_state.page == "Static Data":
        static_data_page()
    elif st.session_state.page == "Dynamic Comparison":
        dynamic_comparison_page()
    elif st.session_state.page == "Settings":
        settings_page()

# --- MAIN ---
def main():
    if not st.session_state.authenticated:
        if 'show_login' not in st.session_state:
            st.session_state.show_login = True
        if st.session_state.show_login:
            login_page()
            if st.button("Don't have an account? Sign up"):
                st.session_state.show_login = False
                st.experimental_rerun()
        else:
            signup_page()
            if st.button("Already have an account? Login"):
                st.session_state.show_login = True
                st.experimental_rerun()
    else:
        main_app()

if __name__ == "__main__":
    main()