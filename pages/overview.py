"""
Overview Dashboard Page - High-level exploration of heavy metals across Switzerland
"""
import streamlit as st
import pandas as pd
from utils.data_utils import calculate_municipality_averages, calculate_national_averages
from utils.chart_utils import (
    create_top_municipalities_chart, 
    create_metal_time_series_chart, 
    create_land_use_breakdown_chart
)
from utils.filter_utils import display_page_header, display_section_header, check_data_availability


def show_overview_page(filtered_df, filters):
    """Display the overview dashboard page"""
    display_page_header(
        "📊 Overview Dashboard", 
        "High-level exploration of heavy metals in soils across Switzerland"
    )
    
    if not check_data_availability(filtered_df):
        return
    
    selected_heavy_metals = filters['heavy_metals']
    
    # 1. Top 5 Municipalities Grid
    display_section_header(
        "🏆 Top 5 Municipalities by Heavy Metal Concentration",
        "Which municipalities have the highest concentrations of each heavy metal?"
    )
    
    # Calculate averages for top municipalities
    muni_averages = calculate_municipality_averages(filtered_df)
    
    # Create small multiple charts for each heavy metal
    cols = st.columns(min(len(selected_heavy_metals), 3))
    for i, metal in enumerate(selected_heavy_metals):
        with cols[i % 3]:
            metal_data = muni_averages[muni_averages['Heavy metal'] == metal].nlargest(5, 'mean')
            
            if not metal_data.empty:
                fig = create_top_municipalities_chart(metal_data, metal)
                if fig:
                    st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # 2. Time Series Comparison
    display_section_header(
        "📈 Time Series Comparison",
        "How do concentrations evolve over time, and how do specific municipalities compare to the average?"
    )
    
    # Calculate yearly averages
    yearly_data = filtered_df.groupby(['Year', 'Heavy metal', 'Municipality'])['Heavy metal concentration (mg/kg DM)'].mean().reset_index()
    national_avg = calculate_national_averages(filtered_df)
    
    # Create time series plots - one for each heavy metal in a grid
    nb_cols = 2
    cols = st.columns(min(len(selected_heavy_metals), nb_cols))
    for i, metal in enumerate(selected_heavy_metals):
        with cols[i % nb_cols]:
            metal_yearly_data = yearly_data[yearly_data['Heavy metal'] == metal]
            metal_national_avg = national_avg[national_avg['Heavy metal'] == metal]
            
            fig = create_metal_time_series_chart(metal_yearly_data, metal_national_avg, metal)
            if fig:
                st.plotly_chart(fig, width="stretch")
    
    st.markdown("---")
    
    # 3. Land Use Breakdown
    display_section_header(
        "🌍 Land Use Breakdown",
        "How does land use affect heavy metal concentrations?"
    )
    
    # Calculate averages by land use and heavy metal
    landuse_data = filtered_df.groupby(['Heavy metal', 'Land use'])['Heavy metal concentration (mg/kg DM)'].mean().reset_index()
    
    fig = create_land_use_breakdown_chart(landuse_data)
    st.plotly_chart(fig, width="stretch")