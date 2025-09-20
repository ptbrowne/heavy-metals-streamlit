"""
Map View Page - Interactive map showing heavy metal concentrations by municipality
"""
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import numpy as np
from utils.data_utils import load_data, get_unique_values
from utils.filter_utils import display_page_header, display_section_header, check_data_availability


@st.cache_data
def load_geocoded_data():
    """Load the geocoded municipalities data"""
    try:
        return pd.read_csv('municipalities_geocoded.csv')
    except FileNotFoundError:
        st.error("⚠️ Geocoded municipalities file not found. Please run the geocoding script first.")
        return None


def calculate_concentration_stats(filtered_df, selected_metal):
    """Calculate concentration statistics for color coding"""
    if filtered_df.empty:
        return None, None, None
    
    concentrations = filtered_df['Heavy metal concentration (mg/kg DM)']
    return concentrations.min(), concentrations.max(), concentrations.quantile([0.25, 0.5, 0.75])


def get_color_for_concentration(concentration, min_val, max_val, quantiles):
    """Get color based on concentration level using quantile-based coloring"""
    if pd.isna(concentration):
        return 'gray'
    
    # Normalize concentration to 0-1 range
    if max_val > min_val:
        normalized = (concentration - min_val) / (max_val - min_val)
    else:
        normalized = 0.5
    
    # Color scale from green (low) to red (high)
    if normalized <= 0.25:
        return '#2ECC71'  # Green
    elif normalized <= 0.5:
        return '#F39C12'  # Orange
    elif normalized <= 0.75:
        return '#E67E22'  # Dark Orange
    else:
        return '#E74C3C'  # Red


def create_map(filtered_df_coords, selected_metal):
    """Create a folium map with heavy metal concentration data"""
    # Filter data for selected metal and year
    
    if filtered_df_coords.empty:
        return None, f"No data available for {selected_metal}"
    
    # Calculate average concentration per municipality for the selected year/metal
    most_recent_year_idx = filtered_df_coords.groupby(['Municipality', 'Latitude', 'Longitude', 'Land use'])['Year'].idxmax()
    map_data = filtered_df_coords.loc[most_recent_year_idx].copy()

    muni_data = map_data.groupby(['Municipality', 'Latitude', 'Longitude', 'Year']).agg({
        'Heavy metal concentration (mg/kg DM)': 'mean',
        'Land use': lambda x: ', '.join(x.unique())
    }).reset_index()
    
    # Calculate color scaling
    min_val, max_val, quantiles = calculate_concentration_stats(map_data, selected_metal)
    
    # Create the base map centered on Switzerland
    center_lat = 46.8182
    center_lon = 8.2275
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=8,
        tiles='OpenStreetMap'
    )
    
    # Add markers for each municipality
    for _, row in muni_data.iterrows():
        concentration = row['Heavy metal concentration (mg/kg DM)']
        color = get_color_for_concentration(concentration, min_val, max_val, quantiles)
        
        # Create popup content
        tooltip_content = f"""
        <div style="width: 200px;">
            <h5>{row['Municipality']}</h5>
            <p>
              <strong>{selected_metal.title()}:</strong> {concentration:.2f} mg/kg DM<br/>
              <strong>Year:</strong> {row['Year']}<br/>
              <strong>Land Use:</strong> {row['Land use']}
            </p>
        </div>
        """
        
        # Determine marker size based on concentration (relative to other values)
        if max_val > min_val:
            size_factor = (concentration - min_val) / (max_val - min_val)
            marker_size = 8 + (size_factor * 15)  # Size between 8 and 23
        else:
            marker_size = 15
        
        folium.CircleMarker(
            location=[row['Latitude'], row['Longitude']],
            radius=marker_size,
            color='white',
            weight=2,
            fillColor=color,
            fillOpacity=0.7,
            tooltip=f"{tooltip_content}"
        ).add_to(m)
    
    # Add a legend
    legend_html = f"""
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 300px; height: 180px; 
                background-color: rgba(255,255,255,0.5); border:0px solid grey; z-index:9999; 
                display: flex; flex-direction: column; justify-content: center;
                backdrop-filter: blur(5px);
                color: black;
                font-size:14px; padding: 10px">
    <h5 style="margin-top:0;">{selected_metal.title()} Concentration</h5>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:#2ECC71"></i> Low (≤ 25th percentile)</p>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:#F39C12"></i> Medium-Low (25-50th)</p>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:#E67E22"></i> Medium-High (50-75th)</p>
    <p style="margin: 5px 0;"><i class="fa fa-circle" style="color:#E74C3C"></i> High (> 75th percentile)</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))
    
    return m, f"Showing {len(muni_data)} municipalities"


def show_map_page(filtered_df, filters):
    """Display the map view page"""
    display_page_header(
        "🗺️ Geographic Distribution", 
        "Interactive map showing heavy metal concentrations across Swiss municipalities"
    )

    selected_metal = filters['heavy_metals'][0] if filters['heavy_metals'] else 'nickel'
    
    # Load data
    data_df = load_data()
    geocoded_df = load_geocoded_data()
    
    if data_df is None or geocoded_df is None:
        return
        
    if not check_data_availability(filtered_df):
        st.warning(f"No data available for {selected_metal} in the selected filters.")
        return
    
    # Merge with geocoded data
    filtered_df_with_coords = filtered_df.merge(
        geocoded_df, 
        on='Municipality', 
        how='inner'
    )
    
    if filtered_df_with_coords.empty:
        st.error("Unable to match municipalities with geographic coordinates.")
        return
    
    # Display summary statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Municipalities", 
            len(filtered_df_with_coords['Municipality'].unique())
        )
    
    with col2:
        avg_concentration = filtered_df_with_coords['Heavy metal concentration (mg/kg DM)'].mean()
        st.metric(
            "Average Concentration", 
            f"{avg_concentration:.2f} mg/kg DM"
        )
    
    with col3:
        max_concentration = filtered_df_with_coords['Heavy metal concentration (mg/kg DM)'].max()
        st.metric(
            "Maximum Concentration", 
            f"{max_concentration:.2f} mg/kg DM"
        )
    
    with col4:
        min_concentration = filtered_df_with_coords['Heavy metal concentration (mg/kg DM)'].min()
        st.metric(
            "Minimum Concentration", 
            f"{min_concentration:.2f} mg/kg DM"
        )
    
    # Create and display the map
    display_section_header(
        f"🎯 {selected_metal.title()} Distribution",
        "Circle size and color represent concentration levels. Click markers for details."
    )
    
    map_obj, status_message = create_map(filtered_df_with_coords, selected_metal)
    
    if map_obj is not None:
        st.info(status_message)
        
        # Display the map
        map_data = st_folium(
            map_obj, 
            width='100%', 
            height=700,
            returned_objects=["last_object_clicked"]
        )
        
        # Show details for clicked municipality
        if map_data['last_object_clicked']:
            clicked_coords = map_data['last_object_clicked']['lat'], map_data['last_object_clicked']['lng']
            
            # Find the municipality that was clicked
            clicked_muni = None
            for _, row in filtered_df_with_coords.iterrows():
                if abs(row['Latitude'] - clicked_coords[0]) < 0.01 and abs(row['Longitude'] - clicked_coords[1]) < 0.01:
                    clicked_muni = row['Municipality']
                    break
            
            if clicked_muni:
                st.subheader(f"📍 Details for {clicked_muni}")
                muni_data = filtered_df_with_coords[filtered_df_with_coords['Municipality'] == clicked_muni]
                
                # Show detailed data for this municipality
                st.dataframe(
                    muni_data[['Sampling Period', 'Land use', 'Heavy metal concentration (mg/kg DM)', 'Sampling date']],
                    hide_index=True
                )
    else:
        st.warning(status_message)
    
    # Additional insights section
    display_section_header(
        "💡 Geographic Insights",
        "Understanding spatial patterns in heavy metal distribution"
    )
    
    # Calculate some basic geographic statistics
    muni_stats = filtered_df_with_coords.groupby('Municipality').agg({
        'Heavy metal concentration (mg/kg DM)': ['mean', 'count']
    }).round(2)
    muni_stats.columns = ['Average Concentration', 'Sample Count']
    muni_stats = muni_stats.reset_index()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔝 Highest Concentrations")
        top_municipalities = muni_stats.nlargest(5, 'Average Concentration')
        for _, row in top_municipalities.iterrows():
            st.write(f"**{row['Municipality']}**: {row['Average Concentration']:.2f} mg/kg DM")
    
    with col2:
        st.markdown("### 🔻 Lowest Concentrations")
        bottom_municipalities = muni_stats.nsmallest(5, 'Average Concentration')
        for _, row in bottom_municipalities.iterrows():
            st.write(f"**{row['Municipality']}**: {row['Average Concentration']:.2f} mg/kg DM")


if __name__ == "__main__":
    show_map_page()