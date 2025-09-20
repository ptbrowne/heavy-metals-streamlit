"""
Data loading and processing utilities for the Heavy Metals Dashboard
"""
import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    """Load and preprocess the heavy metals data"""
    df = pd.read_csv('data.csv')
    
    # Clean the data
    df = df[df['Heavy metal'] != 'Heavy metal']  # Remove header row if it exists
    df['Heavy metal concentration (mg/kg DM)'] = pd.to_numeric(df['Heavy metal concentration (mg/kg DM)'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    
    # Remove rows with missing critical data
    df = df.dropna(subset=['Heavy metal concentration (mg/kg DM)', 'Year'])
    
    # Clean land use names
    df = df[df['Land use'] != 'Land use']  # Remove header row if it exists
    
    return df


@st.cache_data
def get_unique_values(df):
    """Get unique values for filters"""
    municipalities = sorted(df['Municipality'].unique())
    heavy_metals = sorted(df['Heavy metal'].unique())
    land_uses = sorted(df['Land use'].unique())
    year_min = int(df['Year'].min())
    year_max = int(df['Year'].max())
    
    return municipalities, heavy_metals, land_uses, year_min, year_max


def filter_data(df, municipalities, heavy_metals, land_uses, year_range):
    """Filter data based on selected criteria"""
    filtered_df = df.copy()
    
    if municipalities:
        filtered_df = filtered_df[filtered_df['Municipality'].isin(municipalities)]
    if heavy_metals:
        filtered_df = filtered_df[filtered_df['Heavy metal'].isin(heavy_metals)]
    if land_uses:
        filtered_df = filtered_df[filtered_df['Land use'].isin(land_uses)]
    
    filtered_df = filtered_df[
        (filtered_df['Year'] >= year_range[0]) & 
        (filtered_df['Year'] <= year_range[1])
    ]
    
    return filtered_df


def calculate_municipality_averages(df):
    """Calculate average concentrations by municipality and heavy metal"""
    return df.groupby(['Municipality', 'Heavy metal'])['Heavy metal concentration (mg/kg DM)'].agg([
        'mean', 'min', 'max', 'count'
    ]).reset_index()


def calculate_national_averages(df):
    """Calculate national averages by heavy metal and year"""
    return df.groupby(['Heavy metal', 'Year'])['Heavy metal concentration (mg/kg DM)'].mean().reset_index()


def get_data_summary(df):
    """Get summary statistics for the sidebar"""
    return {
        'total_records': len(df),
        'municipalities': len(df['Municipality'].unique()),
        'heavy_metals': len(df['Heavy metal'].unique()),
        'year_range': f"{df['Year'].min():.0f} - {df['Year'].max():.0f}"
    }