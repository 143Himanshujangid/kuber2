import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Any
import io
import base64

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the input dataframe."""
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    
    categorical_cols = df.select_dtypes(include=['object']).columns
    df[categorical_cols] = df[categorical_cols].fillna('Unknown')
    
    return df

def compare_datasets(df1: pd.DataFrame, df2: pd.DataFrame) -> Dict[str, Any]:
    """Compare two datasets and return comparison metrics."""
    comparison = {
        'shape_diff': df1.shape != df2.shape,
        'shape1': df1.shape,
        'shape2': df2.shape,
        'common_columns': list(set(df1.columns) & set(df2.columns)),
        'unique_columns_df1': list(set(df1.columns) - set(df2.columns)),
        'unique_columns_df2': list(set(df2.columns) - set(df1.columns))
    }
    
    if df1.shape == df2.shape:
        comparison['differences'] = (df1 != df2).sum().sum()
        comparison['difference_matrix'] = df1 != df2
    
    return comparison

def create_line_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create an interactive line chart using Plotly."""
    fig = px.line(df, x=x_col, y=y_col, title=title)
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_bar_chart(df: pd.DataFrame, x_col: str, y_col: str, title: str) -> go.Figure:
    """Create an interactive bar chart using Plotly."""
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_pie_chart(df: pd.DataFrame, values_col: str, names_col: str, title: str) -> go.Figure:
    """Create an interactive pie chart using Plotly."""
    fig = px.pie(df, values=values_col, names=names_col, title=title)
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def create_heatmap(df: pd.DataFrame, title: str) -> go.Figure:
    """Create an interactive heatmap using Plotly."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    corr = df[numeric_cols].corr()
    fig = px.imshow(corr, title=title)
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified'
    )
    return fig

def get_download_link(df: pd.DataFrame, filename: str, file_type: str) -> str:
    """Generate a download link for the dataframe."""
    if file_type == 'csv':
        data = df.to_csv(index=False)
        b64 = base64.b64encode(data.encode()).decode()
        href = f'data:file/csv;base64,{b64}'
    elif file_type == 'excel':
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        b64 = base64.b64encode(buffer.getvalue()).decode()
        href = f'data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}'
    else:
        raise ValueError("Unsupported file type")
    
    return f'<a href="{href}" download="{filename}.{file_type}">Download {file_type.upper()} file</a>'

def apply_filters(df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
    """Apply filters to the dataframe."""
    filtered_df = df.copy()
    
    for column, value in filters.items():
        if value is not None and value != '':
            if isinstance(value, (list, tuple)):
                filtered_df = filtered_df[filtered_df[column].isin(value)]
            else:
                filtered_df = filtered_df[filtered_df[column] == value]
    
    return filtered_df 