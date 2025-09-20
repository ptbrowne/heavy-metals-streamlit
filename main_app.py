"""
Swiss Heavy Metals in Soil Dashboard - Main Application
Multi-page Streamlit app using st.navigation and st.Page
"""
import streamlit as st
from utils.data_utils import load_data, get_unique_values, filter_data
from utils.filter_utils import display_sidebar_filters, display_data_summary, display_footer
from pages.overview import show_overview_page
from pages.municipality_detail import show_municipality_detail_page
from pages.heavy_metal_detail import show_heavy_metal_detail_page
from pages.map_view import show_map_page

# Page configuration
st.set_page_config(
    page_title="Swiss Heavy Metals in Soil - Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2E8B57;
        margin-bottom: 2rem;
    }
    .page-header {
        font-size: 2rem;
        color: #4682B4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Load data once at app level
@st.cache_data
def get_app_data():
    """Load and cache app data"""
    df = load_data()
    uniques = get_unique_values(df)
    municipalities = uniques['municipalities']
    heavy_metals = uniques['heavy_metals']
    land_uses = uniques['land_uses']
    year_min = uniques['year_min']
    year_max = uniques['year_max']
    print('app data', municipalities, heavy_metals, land_uses, year_min, year_max)
    return df, municipalities, heavy_metals, land_uses, year_min, year_max

# Initialize data
df, municipalities, heavy_metals, land_uses, year_min, year_max = get_app_data()

# Define page functions
def overview_page():
    """Overview dashboard page"""
    # Create filters specific to overview page
    filters = display_sidebar_filters(municipalities, heavy_metals, land_uses, year_min, year_max, "overview")
    
    # Filter data
    filtered_df = filter_data(df, filters['municipalities'], filters['heavy_metals'], 
                             filters['land_uses'], filters['year_range'])
    
    # Display data summary
    display_data_summary(filtered_df)
    
    # Show overview page content
    show_overview_page(filtered_df, filters)
    
    # Display footer
    display_footer(year_min, year_max, len(municipalities))

def municipality_detail_page():
    """Municipality detail page"""
    # Create filters specific to municipality page
    filters = display_sidebar_filters(municipalities, heavy_metals, land_uses, year_min, year_max, "municipality")
    
    # Filter data
    filtered_df = filter_data(df, filters['municipalities'], filters['heavy_metals'], 
                             filters['land_uses'], filters['year_range'])
    
    # Display data summary
    display_data_summary(filtered_df)
    
    # Show municipality detail page content
    show_municipality_detail_page(filtered_df, filters, df)
    
    # Display footer
    display_footer(year_min, year_max, len(municipalities))

def heavy_metal_detail_page():
    """Heavy metal detail page"""
    # Create filters specific to heavy metal page
    filters = display_sidebar_filters(municipalities, heavy_metals, land_uses, year_min, year_max, "heavy_metal")
    
    # Filter data
    filtered_df = filter_data(df, filters['municipalities'], filters['heavy_metals'], 
                             filters['land_uses'], filters['year_range'])
    
    # Display data summary
    display_data_summary(filtered_df)
    
    # Show heavy metal detail page content
    show_heavy_metal_detail_page(filtered_df, filters)
    
    # Display footer
    display_footer(year_min, year_max, len(municipalities))

def map_view_page():
    """Map view page"""
    filters = display_sidebar_filters(municipalities, heavy_metals, land_uses, year_min, year_max, "map")

    filtered_df = filter_data(df, None, filters['heavy_metals'], 
                             filters['land_uses'], filters['year_range'])

    # Show map page content with built-in filters
    show_map_page(filtered_df, filters)
    
    # Display footer
    display_footer(year_min, year_max, len(municipalities))

# Define pages using st.Page
overview = st.Page(
    overview_page, 
    title="Overview Dashboard", 
    icon="📊",
    default=True
)

municipality_detail = st.Page(
    municipality_detail_page, 
    title="Municipality Detail", 
    icon="🏘️"
)

heavy_metal_detail = st.Page(
    heavy_metal_detail_page, 
    title="Heavy Metal Detail", 
    icon="🧪"
)

map_view = st.Page(
    map_view_page, 
    title="Geographic Map", 
    icon="🗺️"
)

# Create navigation
pg = st.navigation({
    "Analysis": [overview, municipality_detail, heavy_metal_detail, map_view]
})

# App title
st.markdown('<h1 class="main-header">🌱 Swiss Heavy Metals in Soil Dashboard</h1>', unsafe_allow_html=True)

# Run the selected page
pg.run()