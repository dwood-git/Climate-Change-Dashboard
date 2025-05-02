from flask import Flask, render_template, redirect
from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
from graphs.temperature import build_georgia_temperature_graph, build_california_temperature_graph
from graphs.precipitation import build_georgia_precip_graph, build_california_precip_graph
from graphs.vegetation import build_ndvi_graph, build_evi_graph
from graphs.correlations import build_correlation_heatmap, build_drought_line_graph, build_drought_heatmap
from loader import ClimateDataLoader
from dash import exceptions

server = Flask(__name__)
app = Dash(__name__, server=server, url_base_pathname="/dashboard/")
loader = ClimateDataLoader()

df_ga = loader.load_ga_temperature()
df_ca = loader.load_ca_temperature()
df_ga_precip = loader.load_ga_precipitation()
df_ca_precip = loader.load_ca_precipitation()

fig_trends = html.Div([
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
        html.A("View dataset (NOAA Climate Data)", href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
        html.A("View dataset (NOAA Climate Data)", href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
        html.A("View dataset (NOAA Climate Data)", href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
        html.A("View dataset (NOAA Climate Data)", href="https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/statewide/time-series", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
    ], className="graph-card"),
    # Down arrow navigation to Vegetation Indices
    # Up arrow navigation back to Top
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

veg_df = pd.read_csv("data/vegetation/Vegetation_Index_California_Georgia.csv")
fig_veg = html.Div([
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
        html.A("View dataset (MODIS Vegetation Data)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
        html.A("View dataset (MODIS Vegetation Data)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
    # Down arrow navigation to Climate Correlations
    # Up arrow navigation back to Top
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

drought_df = pd.read_csv("data/drought/Drought_Severity_California_Georgia.csv")
ml_df = pd.read_csv("data/california/Fire_Model_California.csv")

fig_corr = html.Div([
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
        html.A("View dataset (US Drought Monitor)", href="https://droughtmonitor.unl.edu/DmData/DataDownload.aspx", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
    ], className="graph-card"),

    # Move the California bubble chart block here
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
        html.Div(id='fire-risk-badge', style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '10px', 'fontWeight': 'bold', 'color': '#d62728'}),
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
        html.A("View dataset (California Fire Perimeters Data) (desktop only)", href="https://data.ca.gov/dataset/california-fire-perimeters-all/resource/b7dd3a39-2163-4a68-9c1a-98ef25d13147", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"}),
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
            "This heatmap visualizes how drought severity varies year by year in Georgia and California. Darker shades represent more severe droughts. It’s useful for spotting prolonged dry periods and identifying environmental stress patterns aligned with fire seasons or vegetation decline.",
            className="graph-subtitle"
        ),
        html.A("View dataset (US Drought Monitor)", href="https://droughtmonitor.unl.edu/DmData/DataDownload.aspx", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
            "This correlation matrix helps identify how strongly climate variables like NDVI, EVI, fire count, and drought severity are related. A higher absolute value means a stronger correlation (positive or negative). It’s a helpful way to quickly see which features tend to change together.",
            className="graph-subtitle"
        ),
        html.A("View dataset (California Fire Perimeters Data) (desktop only)", href="https://data.ca.gov/dataset/california-fire-perimeters-all/resource/b7dd3a39-2163-4a68-9c1a-98ef25d13147", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
        html.A("View dataset (California Fire Perimeters Data) (desktop only)", href="https://data.ca.gov/dataset/california-fire-perimeters-all/resource/b7dd3a39-2163-4a68-9c1a-98ef25d13147", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "20px", "fontSize": "14px", "color": "#1a73e8"})
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
        html.H3("Georgia Wildfire Frequency Map", className="graph-title"),
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
    # Down arrow navigation back to Trends (cycle)
    # Up arrow navigation back to Top
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

app.layout = html.Div([
    html.H1("Wildfire Climate Change Visualization Dashboard", style={"textAlign": "center"}),
    html.P("Visualizing the relationship between climate change and wildfire patterns", style={"textAlign": "center"}),

    html.Div([
        html.Button("🌍 Historical Trends", id="btn-trends", n_clicks=0, className="nav-btn"),
        html.Button("🌿 Vegetation Indices", id="btn-veg", n_clicks=0, className="nav-btn"),
        html.Button("📈 Climate Correlations", id="btn-correlations", n_clicks=0, className="nav-btn"),
    ], className="nav-btn-container"),

    dcc.Store(id='active-tab', data='trends'),
    html.Div(id='tab-content', style={
        'backgroundColor': '#f8f8f8',
        'padding': '30px 15px',
        'margin': '30px auto',
        'borderRadius': '16px',
        'maxWidth': '950px',
        'boxShadow': '0 2px 8px rgba(0,0,0,0.03)'
    }),

    # Go Back to Home Page button
    html.Div([
        html.A("← Back to Home Page", href="/home", style={
            'display': 'block',
            'textAlign': 'center',
            'fontSize': '16px',
            'marginTop': '40px',
            'marginBottom': '10px',
            'color': '#1a73e8',
            'textDecoration': 'none',
            'fontWeight': 'bold'
        })
    ]),

    html.Footer(
        "Built by Dylan Wood | Data sources: NASA, USDM, NOOA, GEE, CAGOV | Honors Project 2025",
        style={
            'textAlign': 'center',
            'fontSize': '13px',
            'marginTop': '40px',
            'marginBottom': '10px',
            'color': '#888'
        }
    ),
])

@app.callback(
    Output('active-tab', 'data'),
    [
        Input('btn-trends', 'n_clicks'),
        Input('btn-veg', 'n_clicks'),
        Input('btn-correlations', 'n_clicks'),
    ]
)
def update_tab(trends, veg, correlations):
    trigger = ctx.triggered_id if ctx.triggered_id else "btn-trends"
    print("Click received. Triggered ID:", trigger)
    return trigger.replace("btn-", "") if trigger.startswith("btn-") else "trends"

@app.callback(
    Output("tab-content", "children"),
    Input("active-tab", "data")
)
def render_tab(tab):
    if tab == "trends":
        return fig_trends
    elif tab == "veg":
        return fig_veg
    elif tab == "correlations":
        return fig_corr
    return html.Div("Select a view above.")



# Callback for California-only bubble chart with year slider and reset button + Fire Risk Badge update
@app.callback(
    [Output("bubble-chart-california", "figure"),
     Output("fire-risk-badge", "children")],
    [Input("year-slider", "value"),
     Input("reset-year-btn", "n_clicks")]
)
def update_bubble_chart(year, reset_clicks):
    color_metric = "FireCount"
    ca_df = ml_df[ml_df["State"] == "California"]
    if ctx.triggered_id == "reset-year-btn":
        filtered_df = ca_df
    else:
        filtered_df = ca_df[ca_df["Year"] == year]

    fig = px.scatter(
        filtered_df,
        x="NDVI",
        y="DroughtSeverity",
        size="FireCount",
        color="FireCount",
        color_continuous_scale=[
            "#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C",
            "#FC4E2A", "#E31A1C", "#BD0026", "#800026"
        ],
        hover_data=["Year", "State"],
        title=None,
        labels={
            "NDVI": "NDVI (Vegetation Health)",
            "DroughtSeverity": "Drought Severity Index",
            "FireCount": "Fires Occurred",
            "Temperature": "Temperature (°F)",
            "FireCount": "Fires Occurred"
        }
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(title='NDVI (Vegetation Health)', range=[0.2, 1.0]),
        yaxis=dict(title='Drought Severity Index', range=[0, 4]),
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )

    # Fire Risk Badge logic
    risk_text = ""
    drought_mean = filtered_df["DroughtSeverity"].mean() if not filtered_df.empty else 0
    ndvi_mean = filtered_df["NDVI"].mean() if not filtered_df.empty else 1
    firecount_mean = filtered_df["FireCount"].mean() if not filtered_df.empty else 0

    if (drought_mean > 2.5) and (ndvi_mean < 0.38) and (firecount_mean > 400):
        risk_text = "🔥 High Risk"
    elif (drought_mean > 1.5) and (ndvi_mean < 0.5) and (firecount_mean > 200):
        risk_text = "⚠️ Moderate Risk"
    else:
        risk_text = "✅ Low Risk"

    return fig, risk_text



# Callback for linked bubble timeline chart: always show full CA data, info panel static
@app.callback(
    [Output("fire-severity-bubble", "figure"),
     Output("info-panel", "children")],
    [Input("bubble-chart-california", "clickData")]
)
def update_linked_line(_):
    df = ml_df[ml_df["State"] == "California"]
    fig = px.scatter(
        df,
        x="Year",
        y="DroughtSeverity",
        size="FireCount",
        color="NDVI",
        color_continuous_scale="YlGn",
        hover_data=["FireCount", "NDVI"],
        labels={
            "Year": "Year",
            "DroughtSeverity": "Drought Index",
            "FireCount": "Fires",
            "NDVI": "NDVI (Vegetation Health)"
        }
    )
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        title_font=dict(family="Arial, sans-serif", size=22),
        font=dict(family="Arial, sans-serif")
    )
    info_text = "Select a bubble to see averages for that year."
    return fig, info_text


# Callback for Satellite Vegetation Comparison dropdown
@app.callback(
    Output("veg-map-display", "children"),
    Input("veg-map-year", "value")
)
def update_veg_maps(year):
    if year == "2001":
        return html.Div([
            # Accessible, text-based NDVI color legend
            html.Div([
                html.H4("NDVI Color Key", style={"textAlign": "center", "color": "#000000", "marginBottom": "10px"}),
                html.P("🟩 Green: Healthy/Dense Vegetation (NDVI > 0.6)", style={"textAlign": "center", "margin": "2px", "color": "#006400"}),
                html.P("🟨 Yellow: Moderate Vegetation (NDVI ≈ 0.4–0.6)", style={"textAlign": "center", "margin": "2px", "color": "#DAA520"}),
                html.P("⬜ White: Low or No Vegetation (NDVI < 0.2)", style={"textAlign": "center", "margin": "2px", "color": "#555555"}),
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("California (2001)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/static/2001_NVDI_CA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for California (2001)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2001-01-01", "2001-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "California")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2001");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("Georgia (2001)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/static/2001_NVDI_GA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for Georgia (2001)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2001-01-01", "2001-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2001");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
            ])
        ])
    elif year == "2022":
        return html.Div([
            # Accessible, text-based NDVI color legend
            html.Div([
                html.H4("NDVI Color Key", style={"textAlign": "center", "color": "#000000", "marginBottom": "10px"}),
                html.P("🟩 Green: Healthy/Dense Vegetation (NDVI > 0.6)", style={"textAlign": "center", "margin": "2px", "color": "#006400"}),
                html.P("🟨 Yellow: Moderate Vegetation (NDVI ≈ 0.4–0.6)", style={"textAlign": "center", "margin": "2px", "color": "#DAA520"}),
                html.P("⬜ White: Low or No Vegetation (NDVI < 0.2)", style={"textAlign": "center", "margin": "2px", "color": "#555555"}),
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("California (2022)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/static/2022_NVDI_CA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for California (2022)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2022-01-01", "2022-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "California")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2022");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("Georgia (2022)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/static/2022_NVDI_GA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for Georgia (2022)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2022-01-01", "2022-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2022");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
            ])
        ])
    else:  # Comparison view
        return html.Div([
            # Accessible, text-based NDVI color legend
            html.Div([
                html.H4("NDVI Color Key", style={"textAlign": "center", "color": "#000000", "marginBottom": "10px"}),
                html.P("🟩 Green: Healthy/Dense Vegetation (NDVI > 0.6)", style={"textAlign": "center", "margin": "2px", "color": "#006400"}),
                html.P("🟨 Yellow: Moderate Vegetation (NDVI ≈ 0.4–0.6)", style={"textAlign": "center", "margin": "2px", "color": "#DAA520"}),
                html.P("⬜ White: Low or No Vegetation (NDVI < 0.2)", style={"textAlign": "center", "margin": "2px", "color": "#555555"}),
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("California: 2001 vs 2022", style={"textAlign": "center", "color": "#000000"}),
                html.Div([
                    html.Div([
                        html.Img(
                            src="/static/2001_NVDI_CA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%", "marginRight": "2%"}),
                    html.Div([
                        html.Img(
                            src="/static/2022_NVDI_CA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%"})
                ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "20px"}),
                html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
            ]),
            html.Div([
                html.H4("Georgia: 2001 vs 2022", style={"textAlign": "center", "color": "#000000"}),
                html.Div([
                    html.Div([
                        html.Img(
                            src="/static/2001_NVDI_GA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%", "marginRight": "2%"}),
                    html.Div([
                        html.Img(
                            src="/static/2022_NVDI_GA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%"})
                ], style={"display": "flex", "justifyContent": "space-between"}),
                html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
            ])
        ])


# Callback to update year-slider value from drought-line-chart click
@app.callback(
    Output('year-slider', 'value'),
    Input('drought-line-chart', 'clickData'),
    prevent_initial_call=True
)
def update_year_from_drought_chart(clickData):
    print("Drought chart clicked:", clickData)
    if clickData and 'points' in clickData and clickData['points']:
        selected_year = clickData['points'][0]['x']
        print("Selected year:", selected_year)
        if isinstance(selected_year, int):
            return selected_year
    raise exceptions.PreventUpdate


# Flask routes
@server.route("/")
def index():
    return redirect("/home")

@server.route("/home")
def landing_page():
    return render_template("landing.html")

if __name__ == "__main__":
    server.run(debug=True, port=8050)