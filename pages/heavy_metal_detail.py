"""
Heavy Metal Detail Page - Deep dive into one heavy metal across all municipalities
"""
import streamlit as st
import pandas as pd
from utils.chart_utils import (
    create_municipality_ranking_chart,
    create_time_evolution_chart,
    create_land_use_box_plot
)
from utils.filter_utils import display_page_header, display_section_header, check_data_availability


def show_heavy_metal_detail_page(filtered_df, filters):
    """Display the heavy metal detail page"""
    selected_heavy_metal_detail = filters.get('selected_heavy_metal_detail')
    if not selected_heavy_metal_detail:
        selected_heavy_metal_detail = filters['heavy_metals'][0] if filters['heavy_metals'] else 'nickel'

    display_page_header(
        f"🧪 {selected_heavy_metal_detail.title()} Detail", 
        "Deep dive across all municipalities."
    )
    
    
    if not check_data_availability(filtered_df):
        return
    
    # Filter data for the selected heavy metal
    metal_data = filtered_df[filtered_df['Heavy metal'] == selected_heavy_metal_detail]
    
    if len(metal_data) == 0:
        st.warning(f"No data available for {selected_heavy_metal_detail}. Please select a different heavy metal.")
        return
        
    col1, col2 = st.columns(2)
    with col1:
        # 1. Municipality Ranking
        display_section_header(
            "🏆 Municipality Ranking",
            "Which municipalities show the highest concentrations of this heavy metal?"
        )
        
        muni_ranking = metal_data.groupby('Municipality')['Heavy metal concentration (mg/kg DM)'].agg([
            'mean', 'count', 'min', 'max', 'std'
        ]).reset_index()
        muni_ranking = muni_ranking.sort_values('mean', ascending=False).head(15)
        
        fig = create_municipality_ranking_chart(muni_ranking, selected_heavy_metal_detail)
        st.plotly_chart(fig, width="stretch")
    
    with col2:
        
        # 2. Time Evolution Across Municipalities
        display_section_header(
            "📈 Time Evolution Across Municipalities",
            "How has this heavy metal changed over time across different municipalities?"
        )
        
        # Get top 8 municipalities for clarity
        top_munis = muni_ranking.head(8)['Municipality'].tolist()
        time_data = metal_data[metal_data['Municipality'].isin(top_munis)]
        
        yearly_trends = time_data.groupby(['Year', 'Municipality'])['Heavy metal concentration (mg/kg DM)'].mean().reset_index()
        
        # Add overall average line
        overall_yearly = metal_data.groupby('Year')['Heavy metal concentration (mg/kg DM)'].mean().reset_index()
        
        fig = create_time_evolution_chart(yearly_trends, overall_yearly, selected_heavy_metal_detail)
        st.plotly_chart(fig, width="stretch")
        
    st.markdown("---")
    
    # 3. Land Use Comparison
    display_section_header(
        "🌍 Land Use Comparison",
        "What's the distribution of this heavy metal across land uses?"
    )
    
    # Create box plot for land use comparison
    fig = create_land_use_box_plot(metal_data, selected_heavy_metal_detail)
    st.plotly_chart(fig, width="stretch")
    
    # Land use statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Land Use Statistics")
        landuse_stats = metal_data.groupby('Land use')['Heavy metal concentration (mg/kg DM)'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std'
        ]).round(2)
        landuse_stats.columns = ['Count', 'Mean', 'Median', 'Min', 'Max', 'Std Dev']
        st.dataframe(landuse_stats, width="stretch")
    
    with col2:
        st.subheader("🔢 Overall Statistics")
        overall_stats = metal_data['Heavy metal concentration (mg/kg DM)'].describe()
        
        # Display as metrics
        st.metric("Total Samples", f"{len(metal_data):,}")
        st.metric("Mean Concentration", f"{overall_stats['mean']:.2f} mg/kg DM")
        st.metric("Median Concentration", f"{overall_stats['50%']:.2f} mg/kg DM")
        st.metric("Standard Deviation", f"{overall_stats['std']:.2f}")
        st.metric("Max Concentration", f"{overall_stats['max']:.2f} mg/kg DM")
        
        # Show municipality with max concentration
        max_idx = metal_data['Heavy metal concentration (mg/kg DM)'].idxmax()
        max_municipality = metal_data.loc[max_idx, 'Municipality']
        st.metric("Highest in Municipality", max_municipality)