# Swiss Heavy Metals in Soil Dashboard

A comprehensive Streamlit dashboard for analyzing heavy metal concentrations in Swiss soils across different municipalities, land uses, and time periods.

## Features

### 📊 Overview Dashboard
- **Top 5 Municipalities Grid**: Small multiple bar charts showing municipalities with highest concentrations for each heavy metal
- **Time Series Comparison**: Line charts comparing municipality trends vs national averages over time
- **Land Use Breakdown**: Stacked bar charts showing how land use affects heavy metal concentrations

### 🏘️ Municipality Detail
- **Municipality Time Series**: Evolution of heavy metals over time for selected municipalities
- **Comparison to National Mean**: How selected municipalities compare to Swiss national trends
- **Land Use Profile**: Heavy metal distribution across different land uses within municipalities

### 🧪 Heavy Metal Detail
- **Municipality Ranking**: Top municipalities with highest concentrations for a specific heavy metal
- **Time Evolution**: Multi-line chart showing how the heavy metal changed across municipalities
- **Land Use Comparison**: Box plots showing distribution across land use types

### Prerequisites
- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone or download the project files
2. Create and activate a virtual environment:
   ```bash
   uv venv streamlit-heavy-metals
   source streamlit-heavy-metals/bin/activate.fish  # For fish shell
   # or: source streamlit-heavy-metals/bin/activate  # For bash/zsh
   ```

3. Install dependencies:
   ```bash
   uv pip install streamlit pandas plotly numpy
   ```

4. Run the application:
   ```bash
   ./streamlit-heavy-metals/bin/streamlit run app.py
   ```

5. Open your browser to `http://localhost:8501`

## Data

The dashboard analyzes data from `data.csv` containing:
- **Heavy Metals**: Cadmium, Chromium, Cobalt, Copper, Lead, Mercury, Nickel, Zinc
- **Time Period**: 1985-2019
- **Locations**: 105+ municipalities across Switzerland
- **Land Uses**: Grassland, Crop cultivation, Various forest types, Urban parks, Protected sites

## Navigation

- Use the **sidebar filters** to customize your analysis
- Switch between pages using the **navigation buttons** at the top
- **Hover over charts** for detailed information and tooltips
- **Multi-select filters** allow comparing multiple municipalities, heavy metals, and land uses

## Key Questions Answered

- Which municipalities have the highest heavy metal concentrations?
- How do concentrations evolve over time?
- How does land use affect heavy metal accumulation?
- How do specific municipalities compare to national averages?
- What are the distribution patterns for specific heavy metals?

## Technical Details

- **Framework**: Streamlit
- **Visualization**: Plotly Express & Plotly Graph Objects
- **Data Processing**: Pandas
- **Caching**: Streamlit's `@st.cache_data` for performance optimization