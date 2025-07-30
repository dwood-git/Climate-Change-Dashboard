"""
Dashboard content components for the wildfire climate change visualization.

This module contains all the HTML/Dash components for different dashboard sections,
including historical trends, vegetation indices, and climate correlations.
"""

from dash import html, dcc
import pandas as pd
from graphs.temperature import build_georgia_temperature_graph, build_california_temperature_graph
from graphs.precipitation import build_georgia_precip_graph, build_california_precip_graph
from graphs.vegetation import build_ndvi_graph, build_evi_graph
from graphs.correlations import build_correlation_heatmap, build_drought_line_graph, build_drought_heatmap


def create_historical_trends_section(data_manager) -> html.Div:
    """
    Create the historical trends section with temperature and precipitation graphs.
    
    Args:
        data_manager: DataManager instance containing all datasets
        
    Returns:
        html.Div: Historical trends section component
    """
    df_ga = data_manager.get_ga_temperature()
    df_ca = data_manager.get_ca_temperature()
    df_ga_precip = data_manager.get_ga_precipitation()
    df_ca_precip = data_manager.get_ca_precipitation()
    
    return html.Div([
        html.Div([
            html.H2("🌍 Historical Trends", className="graph-title"),
            html.P(
                "Visualizing yearly average temperatures and climate trends (1980–2022) for Georgia and California.",
                className="graph-subtitle"
            ),
        ], style={"marginBottom": "10px", "marginTop": "-70px"}),

        html.Div([
            html.H3("Georgia Temperature", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_georgia_temperature_graph(df_ga), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This graph shows Georgia's average yearly temperature from 1980 to 2022, highlighting changes over time.",
                className="graph-subtitle"
            ),
            html.A("View dataset (NOAA Climate Data)", 
                   href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("California Temperature", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_california_temperature_graph(df_ca), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This graph displays California's yearly average temperature, showing warming trends and variability.",
                className="graph-subtitle"
            ),
            html.A("View dataset (NOAA Climate Data)", 
                   href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("Georgia Precipitation", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_georgia_precip_graph(df_ga_precip), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This chart represents Georgia's average annual rainfall, helping us understand water availability trends.",
                className="graph-subtitle"
            ),
            html.A("View dataset (NOAA Climate Data)", 
                   href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("California Precipitation", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_california_precip_graph(df_ca_precip), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This chart shows California's annual rainfall, which can influence droughts and wildfires.",
                className="graph-subtitle"
            ),
            html.A("View dataset (NOAA Climate Data)", 
                   href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        # Navigation back to top
        html.Div([
            html.A("↑ Back to Top", href="#", style={
                "display": "block",
                "textAlign": "center",
                "fontSize": "20px",
                "marginTop": "40px",
                "marginBottom": "20px",
                "color": "#1a73e8",
                "textDecoration": "none",
                "fontWeight": "bold"
            })
        ])
    ], className="section-light")


def create_vegetation_section(data_manager) -> html.Div:
    """
    Create the vegetation indices section with NDVI and EVI graphs.
    
    Args:
        data_manager: DataManager instance containing all datasets
        
    Returns:
        html.Div: Vegetation indices section component
    """
    veg_df = data_manager.get_vegetation_data()
    
    return html.Div([
        html.Div([
            html.H2("🌿 Vegetation Indices", className="graph-title"),
            html.P(
                "Tracking vegetation health using satellite indices NDVI and EVI for Georgia and California.",
                className="graph-subtitle"
            ),
        ], style={"marginBottom": "10px", "marginTop": "-70px"}),
        
        html.Div([
            html.H3("NDVI Line Chart", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_ndvi_graph(veg_df), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "NDVI (Normalized Difference Vegetation Index) indicates vegetation health by measuring greenness from satellite imagery. Higher NDVI values mean denser and healthier plant cover, helping identify drought stress or seasonal changes.",
                className="graph-subtitle"
            ),
            html.A("View dataset (MODIS Vegetation Data)", 
                   href="https://lpdaac.usgs.gov/products/mod13a2v006/", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("EVI Line Chart", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_evi_graph(veg_df), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "EVI (Enhanced Vegetation Index) offers a more accurate look at plant health in areas with dense forests or atmospheric conditions like haze. It adjusts for canopy cover and soil brightness, complementing NDVI for robust vegetation analysis.",
                className="graph-subtitle"
            ),
            html.A("View dataset (MODIS Vegetation Data)", 
                   href="https://lpdaac.usgs.gov/products/mod13a2v006/", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        # Satellite Vegetation Comparison Section
        html.Div([
            html.H3("Satellite Vegetation Comparison", className="graph-title"),
            dcc.Dropdown(
                id="veg-map-year",
                options=[
                    {'label': '2001', 'value': '2001'},
                    {'label': '2022', 'value': '2022'},
                    {'label': 'Comparison', 'value': 'compare'}
                ],
                value='2001',
                clearable=False,
                style={'width': '300px', 'margin': '0 auto 20px', 'color': '#000000'}
            ),
            html.Div(id="veg-map-display")
        ], className="graph-card"),

        # Navigation back to top
        html.Div([
            html.A("↑ Back to Top", href="#", style={
                "display": "block",
                "textAlign": "center",
                "fontSize": "20px",
                "marginTop": "40px",
                "marginBottom": "20px",
                "color": "#1a73e8",
                "textDecoration": "none",
                "fontWeight": "bold"
            })
        ])
    ], className="section-light")


def create_correlations_section(data_manager) -> html.Div:
    """
    Create the climate correlations section with various correlation visualizations.
    
    Args:
        data_manager: DataManager instance containing all datasets
        
    Returns:
        html.Div: Climate correlations section component
    """
    drought_df = data_manager.get_drought_data()
    ml_df = data_manager.get_fire_model_data()
    
    return html.Div([
        html.Div([
            html.H2("📈 Climate Correlations", className="graph-title"),
            html.P(
                "Exploring the relationships between vegetation, drought, temperature, and wildfire activity in California and Georgia.",
                className="graph-subtitle"
            ),
        ], style={"marginBottom": "10px", "marginTop": "-70px"}),
        
        html.Div([
            html.H3("Drought Severity Over Time (GA vs CA)", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(
                        id='drought-line-chart',
                        figure=build_drought_line_graph(drought_df),
                        config={'displayModeBar': False}
                    ),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This chart compares drought severity between Georgia and California over time. Higher values indicate more intense drought conditions. Tracking these trends helps understand long-term stress on ecosystems and how it might contribute to wildfire susceptibility or reduced vegetation growth.",
                className="graph-subtitle"
            ),
            html.A("View dataset (US Drought Monitor)", 
                   href="https://droughtmonitor.unl.edu/DmData/DataDownload.aspx", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        # California bubble chart block
        html.Div([
            html.H3("NDVI, Drought, and Fires (California Only)", className="graph-title"),
            dcc.Slider(
                id='year-slider',
                min=2001,
                max=2022,
                step=1,
                value=2010,
                marks={year: str(year) for year in range(2001, 2023)},
            ),
            html.Button(
                "Show All Years",
                id="reset-year-btn",
                n_clicks=0,
                style={
                    'marginTop': '10px',
                    'marginBottom': '10px',
                    'backgroundColor': '#e0e0e0',
                    'color': '#222',
                    'fontFamily': 'Arial, sans-serif',
                    'borderRadius': '8px',
                    'border': '1px solid #bbb',
                    'padding': '6px 20px',
                    'fontWeight': 'bold'
                }
            ),
            html.Div(id='fire-risk-badge', 
                     style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '10px', 'fontWeight': 'bold', 'color': '#d62728'}),
            dcc.Loading(
                html.Div(
                    dcc.Graph(id='bubble-chart-california', config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "Each bubble represents a year of data for California, plotting vegetation health (NDVI), drought severity, and fire count. Larger, darker bubbles indicate more fires. This visual helps uncover how vegetation loss and drought intensity may relate to wildfire activity over time.",
                className="graph-subtitle"
            ),
            html.A("View dataset (California Fire Perimeters Data) (desktop only)", 
                   href="https://data.ca.gov/dataset/california-fire-perimeters-all/resource/b7dd3a39-2163-4a68-9c1a-98ef25d13147", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"}),
            html.Div(id='info-panel', style={'textAlign': 'center', 'marginTop': '10px', 'fontSize': '14px', 'color': '#333'})
        ], className="graph-card"),

        html.Div([
            html.H3("Drought Severity Heatmap", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_drought_heatmap(drought_df), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This heatmap visualizes how drought severity varies year by year in Georgia and California. Darker shades represent more severe droughts. It's useful for spotting prolonged dry periods and identifying environmental stress patterns aligned with fire seasons or vegetation decline.",
                className="graph-subtitle"
            ),
            html.A("View dataset (US Drought Monitor)", 
                   href="https://droughtmonitor.unl.edu/DmData/DataDownload.aspx", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("Climate Feature Correlation Matrix", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(figure=build_correlation_heatmap(ml_df), config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This correlation matrix helps identify how strongly climate variables like NDVI, EVI, fire count, and drought severity are related. A higher absolute value means a stronger correlation (positive or negative). It's a helpful way to quickly see which features tend to change together.",
                className="graph-subtitle"
            ),
            html.A("View dataset (California Fire Perimeters Data) (desktop only)", 
                   href="https://data.ca.gov/dataset/california-fire-perimeters-all/resource/b7dd3a39-2163-4a68-9c1a-98ef25d13147", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("Fire Severity Bubble Timeline (California)", className="graph-title"),
            dcc.Loading(
                html.Div(
                    dcc.Graph(id='fire-severity-bubble', config={'displayModeBar': False}),
                    className="graph-container"
                ),
                type="circle"
            ),
            html.P(
                "This timeline chart shows how vegetation and fire severity changed year by year in California.",
                className="graph-subtitle"
            ),
            html.A("View dataset (California Fire Perimeters Data) (desktop only)", 
                   href="https://data.ca.gov/dataset/california-fire-perimeters-all/resource/b7dd3a39-2163-4a68-9c1a-98ef25d13147", 
                   target="_blank", 
                   style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
        ], className="graph-card"),

        html.Div([
            html.H3("California Wildfire Frequency Map (2001–2022)", className="graph-title"),
            html.Iframe(
                srcDoc=open("assets/california_fire_map.html", "r").read(),
                width="100%",
                height="600",
                style={
                    'border': 'none',
                    'borderRadius': '12px',
                    'marginTop': '20px',
                    'boxShadow': '0 4px 16px rgba(0,0,0,0.08)'
                }
            ),
            html.P(
                "This interactive map shows cumulative wildfire frequency in California from 2001 to 2022.",
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#000000',
                    'fontSize': '16px',
                    'fontStyle': 'italic',
                    'marginTop': '10px',
                    'marginBottom': '30px'
                }
            )
        ], className="graph-card"),

        html.Div([
            html.H3("Georgia Wildfire Frequency Map (2001-2022)", className="graph-title"),
            html.Img(
                src="/static/ga_firefreq_map.jpg",
                style={
                    'width': '80%',
                    'display': 'block',
                    'margin': '20px auto',
                    'borderRadius': '12px',
                    'boxShadow': '0 4px 16px rgba(0,0,0,0.08)'
                }
            ),
            html.P(
                "Georgia map is based on MODIS Burned Area visualizations, showing cumulative wildfire frequency in the state.",
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#000000',
                    'fontSize': '16px',
                    'fontStyle': 'italic',
                    'marginTop': '10px',
                    'marginBottom': '30px'
                }
            ),
            html.Pre("""// GEE MODIS Burned Area (Georgia)
var burned = ee.ImageCollection("MODIS/061/MCD64A1")
  .filterDate("2001-01-01", "2022-12-31")
  .select("BurnDate")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(burned, 6);
Map.addLayer(burned, {min: 0, max: 366, palette: ['ffffff', 'ff0000']}, "Burned Area");""",
                style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
            html.A(
                "View dataset (MODIS Burned Area - MCD64A1 v6.1)",
                href="https://lpdaac.usgs.gov/products/mcd64a1v061/",
                target="_blank",
                style={
                    "display": "block",
                    "textAlign": "center",
                    "marginBottom": "20px",
                    "fontSize": "14px",
                    "color": "#1a73e8"
                }
            )
        ], className="graph-card"),

        # Navigation back to top
        html.Div([
            html.A("↑ Back to Top", href="#", style={
                "display": "block",
                "textAlign": "center",
                "fontSize": "20px",
                "marginTop": "40px",
                "marginBottom": "20px",
                "color": "#1a73e8",
                "textDecoration": "none",
                "fontWeight": "bold"
            })
        ])
    ], className="section-light") 