"""
Chart creation utilities for the Heavy Metals Dashboard
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def create_top_municipalities_chart(metal_data, metal_name):
    """Create horizontal bar chart for top municipalities by heavy metal"""
    if metal_data.empty:
        return None
        
    fig = px.bar(
        metal_data, 
        x='Municipality', 
        y='mean',
        orientation='v',
        title=f"{metal_name.title()}",
        labels={'mean': 'Avg Concentration (mg/kg DM)', 'Municipality': ''},
        color='mean',
        color_continuous_scale='Reds'
    )
    fig.update_layout(height=300, showlegend=False)
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" +
                    "Avg: %{y:.1f} mg/kg DM<br>" +
                    "<extra></extra>"
    )
    return fig


def create_metal_time_series_chart(yearly_data, national_avg, metal):
    """Create time series comparison chart"""
    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    
    # Add municipality lines
    metal_data = yearly_data[yearly_data['Heavy metal'] == metal]
    
    for municipality in metal_data['Municipality'].unique()[:5]:  # Top 5 municipalities
        muni_data = metal_data[metal_data['Municipality'] == municipality]
        fig.add_trace(go.Scatter(
            x=muni_data['Year'],
            y=muni_data['Heavy metal concentration (mg/kg DM)'],
            mode='lines+markers',
            name=f"{municipality}",
            line=dict(width=2),
            hovertemplate="<b>%{fullData.name}</b><br>" +
                        "Year: %{x}<br>" +
                        "Concentration: %{y:.1f} mg/kg DM<br>" +
                        "<extra></extra>"
        ))
    
    # Add national average line
    nat_data = national_avg[national_avg['Heavy metal'] == metal]
    if not nat_data.empty:
        fig.add_trace(go.Scatter(
            x=nat_data['Year'],
            y=nat_data['Heavy metal concentration (mg/kg DM)'],
            mode='lines',
            name=f"National Avg",
            line=dict(dash='dash', width=3, color='gray'),
            hovertemplate="<b>National Average - %{fullData.name}</b><br>" +
                        "Year: %{x}<br>" +
                        "Concentration: %{y:.1f} mg/kg DM<br>" +
                        "<extra></extra>"
        ))
    
    titlecase_metal = metal.title() if not metal.isupper() else metal
    fig.update_layout(
        title=f"{titlecase_metal} Concentrations Over Time",
        xaxis_title="Year",
        yaxis_title="Concentration (mg/kg DM)",
        hovermode='x unified',
        height=500
    )
    
    return fig


def create_land_use_breakdown_chart(landuse_data):
    """Create stacked bar chart for land use breakdown"""
    fig = px.bar(
        landuse_data,
        x='Heavy metal',
        y='Heavy metal concentration (mg/kg DM)',
        color='Land use',
        title="Average Heavy Metal Concentrations by Land Use",
        labels={'Heavy metal concentration (mg/kg DM)': 'Mean Concentration (mg/kg DM)'},
        barmode='group'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Heavy Metal",
        yaxis_title="Mean Concentration (mg/kg DM)"
    )
    
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                    "Heavy Metal: %{x}<br>" +
                    "Mean Concentration: %{y:.1f} mg/kg DM<br>" +
                    "<extra></extra>"
    )
    
    return fig


def create_municipality_time_series_chart(muni_data, selected_heavy_metals, municipality_names):
    """Create municipality-specific time series chart"""
    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    
    for i, metal in enumerate(selected_heavy_metals):
        metal_data = muni_data[muni_data['Heavy metal'] == metal].sort_values('Year')
        
        fig.add_trace(go.Scatter(
            x=metal_data['Year'],
            y=metal_data['Heavy metal concentration (mg/kg DM)'],
            mode='markers+lines',
            name=metal.title(),
            line=dict(color=colors[i % len(colors)]),
            marker=dict(size=8),
            hovertemplate="<b>%{fullData.name}</b><br>" +
                        "Year: %{x}<br>" +
                        "Concentration: %{y:.1f} mg/kg DM<br>" +
                        "<extra></extra>"
        ))
    
    fig.update_layout(
        title=f"Heavy Metal Evolution Over Time - {', '.join(municipality_names)}",
        xaxis_title="Year",
        yaxis_title="Concentration (mg/kg DM)",
        height=500
    )
    
    return fig


def create_national_comparison_chart(muni_yearly, national_yearly, selected_heavy_metals):
    """Create municipality vs national average comparison chart"""
    fig = go.Figure()
    colors = px.colors.qualitative.Set1
    
    for i, metal in enumerate(selected_heavy_metals):
        muni_metal = muni_yearly[muni_yearly['Heavy metal'] == metal]
        national_metal = national_yearly[national_yearly['Heavy metal'] == metal]
        
        # Municipality line
        fig.add_trace(go.Scatter(
            x=muni_metal['Year'],
            y=muni_metal['Heavy metal concentration (mg/kg DM)'],
            mode='lines+markers',
            name=f"{metal.title()} - Municipality",
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=8)
        ))
        
        # National average line
        fig.add_trace(go.Scatter(
            x=national_metal['Year'],
            y=national_metal['Heavy metal concentration (mg/kg DM)'],
            mode='lines',
            name=f"{metal.title()} - National Average",
            line=dict(color=colors[i % len(colors)], width=2, dash='dash'),
            opacity=0.7
        ))
    
    fig.update_layout(
        title="Municipality vs National Average Trends",
        xaxis_title="Year",
        yaxis_title="Concentration (mg/kg DM)",
        height=500,
        hovermode='x unified'
    )
    
    return fig


def create_land_use_profile_chart(landuse_profile, municipality_names):
    """Create land use profile chart for municipalities"""
    fig = px.bar(
        landuse_profile,
        x='Land use',
        y='Heavy metal concentration (mg/kg DM)',
        color='Heavy metal',
        title=f"Land Use Profile - {', '.join(municipality_names)}",
        labels={'Heavy metal concentration (mg/kg DM)': 'Mean Concentration (mg/kg DM)'},
        barmode='group'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Land Use",
        yaxis_title="Mean Concentration (mg/kg DM)"
    )
    
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +
                    "Land Use: %{x}<br>" +
                    "Mean Concentration: %{y:.1f} mg/kg DM<br>" +
                    "<extra></extra>"
    )
    
    return fig


def create_municipality_ranking_chart(muni_ranking, metal_name):
    """Create horizontal bar chart for municipality ranking"""
    fig = px.bar(
        muni_ranking,
        x='mean',
        y='Municipality',
        orientation='h',
        title=f"Top 15 Municipalities - {metal_name.title()} Concentration",
        labels={'mean': 'Average Concentration (mg/kg DM)', 'Municipality': ''},
        color='mean',
        color_continuous_scale='Reds',
        hover_data=['count', 'min', 'max']
    )
    
    fig.update_layout(
        height=600,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>" +
                    "Avg Concentration: %{x:.1f} mg/kg DM<br>" +
                    "Sample Count: %{customdata[0]}<br>" +
                    "Min: %{customdata[1]:.1f} mg/kg DM<br>" +
                    "Max: %{customdata[2]:.1f} mg/kg DM<br>" +
                    "<extra></extra>"
    )
    
    return fig


def create_time_evolution_chart(yearly_trends, overall_yearly, metal_name):
    """Create time evolution chart for heavy metal across municipalities"""
    fig = px.line(
        yearly_trends,
        x='Year',
        y='Heavy metal concentration (mg/kg DM)',
        color='Municipality',
        title=f"{metal_name.title()} Evolution Over Time (Top 8 Municipalities)",
        markers=True
    )
    
    # Add overall average line
    fig.add_trace(go.Scatter(
        x=overall_yearly['Year'],
        y=overall_yearly['Heavy metal concentration (mg/kg DM)'],
        mode='lines',
        name='Overall Average',
        line=dict(dash='dash', width=3, color='black'),
        hovertemplate="<b>Overall Average</b><br>" +
                    "Year: %{x}<br>" +
                    "Concentration: %{y:.1f} mg/kg DM<br>" +
                    "<extra></extra>"
    ))
    
    fig.update_layout(
        height=500,
        xaxis_title="Year",
        yaxis_title="Concentration (mg/kg DM)"
    )
    
    return fig


def create_land_use_box_plot(metal_data, metal_name):
    """Create box plot for land use comparison"""
    fig = px.box(
        metal_data,
        x='Land use',
        y='Heavy metal concentration (mg/kg DM)',
        title=f"{metal_name.title()} Distribution by Land Use",
        color='Land use'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Land Use",
        yaxis_title="Concentration (mg/kg DM)",
        showlegend=False
    )
    
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" +
                    "Concentration: %{y:.1f} mg/kg DM<br>" +
                    "<extra></extra>"
    )
    
    return fig