# Query Parameter Implementation

## Overview
I've successfully implemented query parameter support for your Streamlit Heavy Metals Dashboard using `st.query_params`. The implementation allows users to:

1. **Bookmark filter states**: URLs now contain all filter settings
2. **Share filtered views**: Send URLs to colleagues with specific filters applied
3. **Navigate between pages**: Filter settings are preserved across page navigation
4. **Deep linking**: Direct access to specific filter combinations

## Implementation Details

### New Functions Added

1. **`get_filters_from_query_params()`**
   - Extracts filter values from URL query parameters
   - Handles comma-separated values for multi-select filters
   - Includes error handling for malformed data

2. **`update_query_params(filters)`**
   - Updates URL query parameters when filters change
   - Automatically called when filter values are modified
   - Handles empty/null values appropriately

### Modified Functions

**`display_sidebar_filters()`** - Enhanced to:
- Read initial values from query parameters
- Set appropriate defaults when query params are invalid
- Automatically update query parameters when filters change
- Maintain unique keys for Streamlit widgets to avoid conflicts

## Query Parameter Format

The URL query parameters follow this format:
```
?municipalities=Zurich,Basel,Geneva&heavy_metals=Cadmium,Lead&land_uses=Agricultural,Urban&year_range=2010,2020&selected_heavy_metal_detail=Cadmium
```

### Parameter Details:
- `municipalities`: Comma-separated municipality names
- `heavy_metals`: Comma-separated heavy metal names
- `land_uses`: Comma-separated land use types
- `year_range`: "min_year,max_year" format
- `selected_heavy_metal_detail`: Single heavy metal name for detail page

## Benefits

1. **User Experience**: Filters persist across page navigation
2. **Collaboration**: Easy sharing of specific filter combinations
3. **Bookmarking**: Users can save specific dashboard states
4. **Deep Linking**: Direct access to filtered views from external links
5. **Analytics**: Track which filter combinations are most popular

## Error Handling

The implementation includes robust error handling for:
- Invalid municipality/heavy metal names not in dataset
- Malformed year ranges
- Empty or missing query parameters
- Widget key conflicts

## Testing

To test the implementation:
1. Run the Streamlit app: `streamlit run main_app.py`
2. Change some filters in the sidebar
3. Observe the URL updating with query parameters
4. Copy the URL and paste it in a new browser tab
5. Verify that filters are restored to the previous state
6. Navigate between pages and confirm filters persist

The implementation is backward compatible and will work seamlessly with existing functionality while adding the new query parameter features.