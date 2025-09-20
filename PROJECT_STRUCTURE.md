# Project Structure

## Overview
This project has been refactored into a modern multi-page Streamlit application using `st.navigation` and `st.Page`. The code is now organized into separate modules for better maintainability and scalability.

## Directory Structure

```
/Users/patrick/code/maureen-notebooks/strealit-proto-heavy/
├── main_app.py                 # Main application entry point (NEW)
├── app.py                      # Legacy single-page app (DEPRECATED)
├── data.csv                    # Heavy metals dataset
├── requirements.txt            # Python dependencies
├── README.md                   # Main documentation
├── spec.md                     # Original specification
├── streamlit-heavy-metals/     # Virtual environment
├── utils/                      # Utility modules (NEW)
│   ├── data_utils.py          # Data loading and processing functions
│   ├── chart_utils.py         # Chart creation utilities
│   └── filter_utils.py        # Filter and UI utilities
└── pages/                      # Page modules (NEW)
    ├── overview.py            # Overview dashboard page
    ├── municipality_detail.py # Municipality analysis page
    └── heavy_metal_detail.py  # Heavy metal analysis page
```

## Architecture

### 1. Main Application (`main_app.py`)
- **Entry Point**: Uses modern `st.navigation` and `st.Page` structure
- **Page Routing**: Defines page functions and navigation
- **Global State**: Loads and caches data once for all pages
- **Common Elements**: Applies CSS styling and page configuration

### 2. Utility Modules (`utils/`)

#### `data_utils.py`
- `load_data()`: Load and preprocess CSV data with caching
- `get_unique_values()`: Extract filter options from data
- `filter_data()`: Apply user-selected filters
- `calculate_municipality_averages()`: Aggregate data by municipality
- `calculate_national_averages()`: Calculate national trends
- `get_data_summary()`: Generate sidebar statistics

#### `chart_utils.py`
- Chart creation functions for all visualizations
- Plotly-based interactive charts with consistent styling
- Hover templates and responsive design
- Functions for each chart type (bar, line, box plots, etc.)

#### `filter_utils.py`
- `create_sidebar_filters()`: Generate dynamic filter widgets
- `display_data_summary()`: Show data metrics in sidebar
- `check_data_availability()`: Validate filtered data
- UI helper functions for consistent page structure

### 3. Page Modules (`pages/`)

#### `overview.py`
- **Top 5 Municipalities Grid**: Small multiple bar charts
- **Time Series Comparison**: Municipality vs national trends
- **Land Use Breakdown**: How land use affects concentrations

#### `municipality_detail.py`
- **Municipality Time Series**: Evolution over time
- **National Comparison**: Municipality vs Swiss average
- **Land Use Profile**: Land use analysis for selected municipalities
- **Summary Statistics**: Detailed statistical breakdown

#### `heavy_metal_detail.py`
- **Municipality Ranking**: Top 15 municipalities by concentration
- **Time Evolution**: Heavy metal trends across municipalities
- **Land Use Comparison**: Distribution analysis with box plots
- **Comprehensive Statistics**: Overall and land-use specific metrics

## Key Improvements

### 1. **Modern Streamlit Architecture**
- Uses `st.navigation()` and `st.Page()` for proper multi-page apps
- Cleaner URL routing and page management
- Better user experience with consistent navigation

### 2. **Modular Design**
- Separated concerns into logical modules
- Reusable utility functions
- Easier testing and maintenance

### 3. **Performance Optimization**
- Data loaded once and cached at app level
- Efficient filtering and aggregation functions
- Reduced redundant computations

### 4. **Code Organization**
- Clear separation between data processing, visualization, and UI
- Consistent function signatures and documentation
- Better code reusability

## Running the Application

### New Multi-page App (Recommended)
```bash
./streamlit-heavy-metals/bin/streamlit run main_app.py
```

### Legacy Single-page App (Deprecated)
```bash
./streamlit-heavy-metals/bin/streamlit run app.py
```

## Development Guidelines

### Adding New Pages
1. Create a new file in `pages/` directory
2. Implement the page function following existing patterns
3. Add the page to navigation in `main_app.py`

### Adding New Charts
1. Add chart creation function to `chart_utils.py`
2. Follow consistent parameter patterns and hover templates
3. Use the existing color schemes and styling

### Adding New Filters
1. Extend `create_sidebar_filters()` in `filter_utils.py`
2. Update page functions to handle new filter parameters
3. Ensure proper data validation

## Migration Notes

The legacy `app.py` has been preserved for reference but should not be used for new development. All new features should be added to the modular structure in `main_app.py` and associated modules.

## Future Enhancements

1. **Data Export**: Add CSV/Excel export functionality
2. **Advanced Filters**: Implement date range pickers and numeric filters
3. **Custom Analysis**: Allow users to create custom chart combinations
4. **Performance**: Add data sampling for large datasets
5. **Testing**: Implement unit tests for utility functions