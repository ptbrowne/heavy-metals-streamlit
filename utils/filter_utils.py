"""
Filter and UI utilities for the Heavy Metals Dashboard

Query Parameter Support:
- The filters automatically save and restore their state using Streamlit's query parameters
- URL format: ?municipalities=A,B,C&heavy_metals=X,Y&land_uses=L1,L2&year_range=2010,2020&selected_heavy_metal_detail=X
- Users can bookmark URLs with specific filter settings
- Sharing URLs preserves the current filter state
- Navigation between pages maintains filter settings

Supported query parameters:
- municipalities: comma-separated list of municipality names
- heavy_metals: comma-separated list of heavy metal names  
- land_uses: comma-separated list of land use types
- year_range: "min_year,max_year" format
- selected_heavy_metal_detail: single heavy metal name for detail page
"""
import streamlit as st
import json


def get_filters_from_query_params():
    """Extract filter values from query parameters"""
    query_params = st.query_params
    filters = {}
    
    # Extract municipalities (stored as comma-separated string)
    if 'municipalities' in query_params:
        municipalities_str = query_params['municipalities']
        if municipalities_str:  # Check if not empty
            filters['municipalities'] = [m.strip() for m in municipalities_str.split(',') if m.strip()]
    
    # Extract heavy metals (stored as comma-separated string)
    if 'heavy_metals' in query_params:
        heavy_metals_str = query_params['heavy_metals']
        if heavy_metals_str:  # Check if not empty
            filters['heavy_metals'] = [m.strip() for m in heavy_metals_str.split(',') if m.strip()]
    
    # Extract land uses (stored as comma-separated string)
    if 'land_uses' in query_params:
        land_uses_str = query_params['land_uses']
        if land_uses_str:  # Check if not empty
            filters['land_uses'] = [l.strip() for l in land_uses_str.split(',') if l.strip()]
    
    # Extract year range (stored as "min,max")
    if 'year_range' in query_params:
        year_range_str = query_params['year_range']
        try:
            year_min, year_max = year_range_str.split(',')
            filters['year_range'] = (int(year_min.strip()), int(year_max.strip()))
        except (ValueError, AttributeError):
            pass
    
    # Extract selected heavy metal for detail page
    if 'selected_heavy_metal_detail' in query_params:
        filters['selected_heavy_metal_detail'] = query_params['selected_heavy_metal_detail'].strip()
    
    return filters


def update_query_params(filters):
    """Update query parameters based on current filter values"""
    try:
        # Update municipalities
        if filters.get('municipalities'):
            st.query_params['municipalities'] = ','.join(filters['municipalities'])
        else:
            if 'municipalities' in st.query_params:
                del st.query_params['municipalities']
        
        # Update heavy metals
        if filters.get('heavy_metals'):
            st.query_params['heavy_metals'] = ','.join(filters['heavy_metals'])
        else:
            if 'heavy_metals' in st.query_params:
                del st.query_params['heavy_metals']
        
        # Update land uses
        if filters.get('land_uses'):
            st.query_params['land_uses'] = ','.join(filters['land_uses'])
        else:
            if 'land_uses' in st.query_params:
                del st.query_params['land_uses']
        
        # Update year range
        if filters.get('year_range'):
            year_min, year_max = filters['year_range']
            st.query_params['year_range'] = f"{year_min},{year_max}"
        
        # Update selected heavy metal detail
        if filters.get('selected_heavy_metal_detail'):
            st.query_params['selected_heavy_metal_detail'] = filters['selected_heavy_metal_detail']
        else:
            if 'selected_heavy_metal_detail' in st.query_params:
                del st.query_params['selected_heavy_metal_detail']
    except Exception as e:
        # If there's an error updating query params, continue without crashing
        st.sidebar.error(f"Error updating URL parameters: {str(e)}")
        pass


def display_sidebar_filters(municipalities, heavy_metals, land_uses, year_min, year_max, page_type="overview"):
    """Create sidebar filters for the dashboard"""
    st.sidebar.header("🔍 Filters")
    
    # Get current filter values from query parameters
    saved_filters = get_filters_from_query_params()
    
    # Page-specific filters
    additional_filters = {}
    
    selected_municipalities = []
    if page_type == "municipality":
        # Get default from query params or use first municipality
        default_municipalities = saved_filters.get('municipalities', [municipalities[0]] if municipalities else [])
        # Ensure default municipalities exist in the available options
        default_municipalities = [m for m in default_municipalities if m in municipalities]
        if not default_municipalities and municipalities:
            default_municipalities = [municipalities[0]]
            
        selected_municipalities = st.sidebar.multiselect(
            "Select Municipalities for Detail Analysis:",
            options=municipalities,
            default=default_municipalities,
            help="Select municipalities for detailed analysis",
            key="municipalities_detail"
        )
    
    elif page_type == "heavy_metal":
        st.sidebar.subheader("Heavy Metal-specific filters")
        # Get default from query params or use first heavy metal
        default_heavy_metal = saved_filters.get('selected_heavy_metal_detail', heavy_metals[0] if heavy_metals else None)
        # Ensure default heavy metal exists in the available options
        if default_heavy_metal not in heavy_metals and heavy_metals:
            default_heavy_metal = heavy_metals[0]
            
        selected_heavy_metal_detail = st.sidebar.selectbox(
            "Select Heavy Metal for Detail Analysis:",
            options=heavy_metals,
            index=heavy_metals.index(default_heavy_metal) if default_heavy_metal in heavy_metals else 0,
            help="Select one heavy metal for detailed analysis",
            key="heavy_metal_detail"
        )
        additional_filters['selected_heavy_metal_detail'] = selected_heavy_metal_detail

    # Common filters for all pages
    if not selected_municipalities:
        # Get default from query params
        default_municipalities = saved_filters.get('municipalities', [])
        # Ensure default municipalities exist in the available options
        default_municipalities = [m for m in default_municipalities if m in municipalities]
        
        selected_municipalities = st.sidebar.multiselect(
            "Select Municipalities:",
            options=municipalities,
            default=default_municipalities,
            help="Leave empty to include all municipalities",
            key="municipalities_common"
        )
    
    if page_type == "overview" or page_type == 'municipality':
        # Get default from query params or use first 3 heavy metals
        default_heavy_metals = saved_filters.get('heavy_metals', heavy_metals[:3] if len(heavy_metals) >= 3 else heavy_metals)
        # Ensure default heavy metals exist in the available options
        default_heavy_metals = [m for m in default_heavy_metals if m in heavy_metals]
        if not default_heavy_metals and heavy_metals:
            default_heavy_metals = heavy_metals[:3]
            
        selected_heavy_metals = st.sidebar.multiselect(
            "Select Heavy Metals:",
            options=heavy_metals,
            default=default_heavy_metals,
            help="Select one or more heavy metals to analyze",
            key="heavy_metals_common"
        )
    else:
        selected_heavy_metals = []
    
    # Get default from query params
    default_land_uses = saved_filters.get('land_uses', [])
    # Ensure default land uses exist in the available options
    default_land_uses = [l for l in default_land_uses if l in land_uses]
        
    selected_land_uses = st.sidebar.multiselect(
        "Select Land Uses:",
        options=land_uses,
        default=default_land_uses,
        help="Leave empty to include all land uses",
        key="land_uses_common"
    )
    
    # Get default year range from query params
    default_year_range = saved_filters.get('year_range', (year_min, year_max))
    # Ensure the default year range is within bounds
    default_year_range = (
        max(default_year_range[0], year_min),
        min(default_year_range[1], year_max)
    )
    
    year_range = st.sidebar.slider(
        "Year Range:",
        min_value=year_min,
        max_value=year_max,
        value=default_year_range,
        help="Select the time period for analysis",
        key="year_range_slider"
    )
    
    # Prepare filters dictionary
    current_filters = {
        'municipalities': selected_municipalities,
        'heavy_metals': selected_heavy_metals,
        'land_uses': selected_land_uses,
        'year_range': year_range,
        **additional_filters
    }
    
    # Update query parameters with current filter values
    update_query_params(current_filters)
    
    return current_filters


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
### About This Dashboard

This dashboard provides comprehensive analysis of heavy metal concentrations in Swiss soils. 
The data includes measurements from various municipalities across different land uses and time periods.

**Heavy Metals Analyzed:** Cadmium, Chromium, Cobalt, Copper, Lead, Mercury, Nickel, Zinc

**Data Period:** {year_min} - {year_max}

**Municipalities:** {num_municipalities} locations across Switzerland

💡 **Usage Tips:**
- Use the sidebar filters to customize your analysis
- Navigate between pages using the menu
- Hover over charts for detailed information
- Compare multiple municipalities and heavy metals simultaneously
    """)
