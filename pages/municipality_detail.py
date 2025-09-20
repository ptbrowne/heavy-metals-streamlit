"""
Municipality Detail Page - Deep dive into one or more municipalities
"""
import streamlit as st
import pandas as pd
from utils.data_utils import calculate_national_averages
from utils.chart_utils import (
    create_municipality_time_series_chart,
    create_national_comparison_chart,
    create_land_use_profile_chart
)
from utils.filter_utils import display_page_header, display_section_header, check_data_availability


def show_municipality_detail_page(filtered_df, filters, full_df):
    """Display the municipality detail page"""
    display_page_header(
        "🏘️ Municipality Detail", 
        "Deep dive into one or more municipalities"
    )
    
    selected_municipalities = filters['municipalities']
    selected_heavy_metals = filters['heavy_metals']
    
    if not selected_municipalities:
        st.warning("Please select at least one municipality from the sidebar to view detailed analysis.")
        return
    elif not check_data_availability(filtered_df):
        return
    
    # Display selected municipalities
    st.info(f"Analyzing: {', '.join(selected_municipalities)}")
    
    # Filter data for selected municipalities
    muni_data = filtered_df[filtered_df['Municipality'].isin(selected_municipalities)]
    
    # 1. Municipality Time Series
    display_section_header(
        "📈 Municipality Time Series",
        "How has each heavy metal evolved in this municipality over time?"
    )
    
    fig = create_municipality_time_series_chart(muni_data, selected_heavy_metals, selected_municipalities)
    st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # 2. Comparison to National Mean
    display_section_header(
        "🇨🇭 Comparison to National Mean",
        "How does this municipality compare to the overall Swiss trend?"
    )
    
    # Calculate municipality averages by year
    muni_yearly = muni_data.groupby(['Year', 'Heavy metal'])['Heavy metal concentration (mg/kg DM)'].mean().reset_index()
    national_yearly = calculate_national_averages(full_df)  # Use full dataset for national average
    
    fig = create_national_comparison_chart(muni_yearly, national_yearly, selected_heavy_metals)
    st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # 3. Land Use Profile
    display_section_header(
        "🌱 Land Use Profile",
        "Which land uses in this municipality accumulate more heavy metals?"
    )
    
    landuse_profile = muni_data.groupby(['Land use', 'Heavy metal'])['Heavy metal concentration (mg/kg DM)'].mean().reset_index()
    
    if not landuse_profile.empty:
        fig = create_land_use_profile_chart(landuse_profile, selected_municipalities)
        st.plotly_chart(fig, width="stretch")
        
        # Summary statistics table
        st.subheader("📊 Summary Statistics")
        summary_stats = muni_data.groupby(['Heavy metal', 'Land use'])['Heavy metal concentration (mg/kg DM)'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        
        st.dataframe(summary_stats, width="stretch")
    else:
        st.warning("No land use data available for the selected municipalities and filters.")