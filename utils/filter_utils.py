"""
Filter and UI utilities for the Heavy Metals Dashboard
"""
import streamlit as st


def display_sidebar_filters(municipalities, heavy_metals, land_uses, year_min, year_max, page_type="overview"):
    """Create sidebar filters for the dashboard"""
    st.sidebar.header("🔍 Filters")
    
    # Common filters for all pages
    selected_municipalities = st.sidebar.multiselect(
        "Select Municipalities:",
        options=municipalities,
        default=[],
        help="Leave empty to include all municipalities"
    )
    
    selected_heavy_metals = st.sidebar.multiselect(
        "Select Heavy Metals:",
        options=heavy_metals,
        default=heavy_metals[:3],  # Default to first 3 heavy metals
        help="Select one or more heavy metals to analyze"
    )
    
    selected_land_uses = st.sidebar.multiselect(
        "Select Land Uses:",
        options=land_uses,
        default=[],
        help="Leave empty to include all land uses"
    )
    
    year_range = st.sidebar.slider(
        "Year Range:",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        help="Select the time period for analysis"
    )
    
    # Page-specific filters
    additional_filters = {}
    
    if page_type == "municipality":
        st.sidebar.subheader("Municipality-specific filters")
        if not selected_municipalities:
            selected_municipalities = st.sidebar.multiselect(
                "Select Municipalities for Detail Analysis:",
                options=municipalities,
                default=[municipalities[0]] if municipalities else [],
                help="Select municipalities for detailed analysis"
            )
    
    elif page_type == "heavy_metal":
        st.sidebar.subheader("Heavy Metal-specific filters")
        selected_heavy_metal_detail = st.sidebar.selectbox(
            "Select Heavy Metal for Detail Analysis:",
            options=selected_heavy_metals if selected_heavy_metals else heavy_metals,
            help="Select one heavy metal for detailed analysis"
        )
        additional_filters['selected_heavy_metal_detail'] = selected_heavy_metal_detail
    
    return {
        'municipalities': selected_municipalities,
        'heavy_metals': selected_heavy_metals,
        'land_uses': selected_land_uses,
        'year_range': year_range,
        **additional_filters
    }


def display_data_summary(filtered_df):
    """Display data summary in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Data Summary")
    st.sidebar.metric("Total Records", len(filtered_df))
    st.sidebar.metric("Municipalities", len(filtered_df['Municipality'].unique()))
    st.sidebar.metric("Heavy Metals", len(filtered_df['Heavy metal'].unique()))
    st.sidebar.metric("Years Covered", f"{filtered_df['Year'].min():.0f} - {filtered_df['Year'].max():.0f}")


def check_data_availability(filtered_df, context=""):
    """Check if data is available and show appropriate warnings"""
    if len(filtered_df) == 0:
        st.warning(f"No data available for the selected filters{' for ' + context if context else ''}. Please adjust your selection.")
        return False
    return True


def display_page_header(title, description):
    """Display page header with title and description"""
    st.markdown(f'<h2 class="page-header">{title}</h2>', unsafe_allow_html=True)
    st.markdown(description)


def display_section_header(title, question):
    """Display section header with title and question"""
    st.subheader(title)
    st.markdown(f"*{question}*")


def display_footer(year_min, year_max, num_municipalities):
    """Display app footer with information"""
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <h4>About This Dashboard</h4>
        <p>This dashboard provides comprehensive analysis of heavy metal concentrations in Swiss soils. 
        The data includes measurements from various municipalities across different land uses and time periods.</p>
        
        <p><strong>Heavy Metals Analyzed:</strong> Cadmium, Chromium, Cobalt, Copper, Lead, Mercury, Nickel, Zinc</p>
        <p><strong>Data Period:</strong> {year_min} - {year_max}</p>
        <p><strong>Municipalities:</strong> {num_municipalities} locations across Switzerland</p>
        
        <p style="font-size: 0.9em; margin-top: 1rem;">
            💡 <strong>Usage Tips:</strong><br>
            • Use the sidebar filters to customize your analysis<br>
            • Navigate between pages using the menu<br>
            • Hover over charts for detailed information<br>
            • Compare multiple municipalities and heavy metals simultaneously
        </p>
    </div>
    """, unsafe_allow_html=True)