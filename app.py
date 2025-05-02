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

        html.Div([
            html.H3("Georgia Temperature", className="graph-title"),
            dcc.Loading(
                dcc.Graph(figure=build_georgia_temperature_graph(df_ga), config={'displayModeBar': False}),
                type="circle"
            ),
        ], className="graph-card"),

        html.Div([
            html.H3("California Temperature", className="graph-title"),
            dcc.Loading(
                dcc.Graph(figure=build_california_temperature_graph(df_ca), config={'displayModeBar': False}),
                type="circle"
            ),
        ], className="graph-card"),

        html.Div([
            html.H3("Georgia Precipitation", className="graph-title"),
            dcc.Loading(
                dcc.Graph(figure=build_georgia_precip_graph(df_ga_precip), config={'displayModeBar': False}),
                type="circle"
            ),
        ], className="graph-card"),

        html.Div([
            html.H3("California Precipitation", className="graph-title"),
            dcc.Loading(
                dcc.Graph(figure=build_california_precip_graph(df_ca_precip), config={'displayModeBar': False}),
                type="circle"
            ),
        ], className="graph-card"),
    ], className="section-light")
])

veg_df = pd.read_csv("data/vegetation/Vegetation_Index_California_Georgia.csv")
fig_veg = html.Div([
    html.Div([
        html.H3("NDVI Line Chart", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_ndvi_graph(veg_df), config={'displayModeBar': False}),
            type="circle"
        ),
    ], className="graph-card"),

    html.Div([
        html.H3("EVI Line Chart", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_evi_graph(veg_df), config={'displayModeBar': False}),
            type="circle"
        ),
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
], className="section-light")

drought_df = pd.read_csv("data/drought/Drought_Severity_California_Georgia.csv")
ml_df = pd.read_csv("data/california/Fire_Model_California.csv")

fig_corr = html.Div([
    html.Div([
        html.H3("Drought Severity Over Time (GA vs CA)", className="graph-title"),
        dcc.Loading(
            dcc.Graph(
                id='drought-line-chart',
                figure=build_drought_line_graph(drought_df),
                config={'displayModeBar': False}
            ),
            type="circle"
        ),
    ], className="graph-card"),

    html.Div([
        html.H3("Drought Severity Heatmap", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_drought_heatmap(drought_df), config={'displayModeBar': False}),
            type="circle"
        ),
    ], className="graph-card"),

    html.Div([
        html.H3("Climate Feature Correlation Matrix", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_correlation_heatmap(ml_df), config={'displayModeBar': False}),
            type="circle"
        ),
    ], className="graph-card"),

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
        dcc.Dropdown(
            id='bubble-axis-selector',
            options=[
                {'label': 'NDVI vs DroughtSeverity', 'value': 'ndvi_drought'},
                {'label': 'EVI vs FireCount', 'value': 'evi_fire'},
                {'label': 'Temperature vs Drought', 'value': 'temp'}
            ],
            value='ndvi_drought',
            clearable=False,
            style={'width': '300px', 'margin': '10px auto'}
        ),
        dcc.Dropdown(
            id='bubble-color-metric',
            options=[
                {'label': 'Fires Occured', 'value': 'FireCount'}
            ],
            value='FireCount',
            clearable=False,
            style={'width': '200px', 'margin': '10px auto'}
        ),
        html.Div(id='fire-risk-badge', style={'textAlign': 'center', 'fontSize': '18px', 'marginTop': '10px', 'fontWeight': 'bold', 'color': '#d62728'}),
        dcc.Loading(
            dcc.Graph(id='bubble-chart-california', config={'displayModeBar': False}),
            type="circle"
        ),
        
        html.Div(id='info-panel', style={'textAlign': 'center', 'marginTop': '10px', 'fontSize': '14px', 'color': '#333'})
    ], className="graph-card"),

    html.Div([
        html.H3("Fire Severity Bubble Timeline (California)", className="graph-title"),
        dcc.Loading(
            dcc.Graph(id='fire-severity-bubble', config={'displayModeBar': False}),
            type="circle"
        ),
    ], className="graph-card"),

    html.Div([
        html.H3("California Wildfire Frequency Map (2001–2022)", className="graph-title"),
        html.Iframe(
            srcDoc=open("assets/maps/california_fire_map.html", "r").read(),
            width="100%",
            height="600",
            style={
                'border': 'none',
                'marginTop': '20px',
                'boxShadow': '0 4px 16px rgba(0,0,0,0.08)',
                'borderRadius': '12px',
                'display': 'block'
            }
        ),
        html.P(
            "This interactive map overlays fire frequency across California, highlighting regions with repeated wildfire events from 2001 to 2022.",
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
        html.H3("Georgia Wildfire Frequency Map (Screenshot Reference)", className="graph-title"),
        html.Img(
            src="/assets/ga_firefreq_map.jpg",
            style={
                'width': '80%',
                'display': 'block',
                'margin': '20px auto',
                'borderRadius': '12px',
                'boxShadow': '0 4px 16px rgba(0,0,0,0.08)'
            }
        ),
        html.P(
            "Georgia map is based on MODIS Burned Area visualizations (Screenshot Version), showing cumulative wildfire frequency in the state.",
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

    html.Footer(
        "Built by Dylan Wood | Data sources: NASA, USGS, ERA5, USDM | Honors Project 2025",
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
     Input("reset-year-btn", "n_clicks"),
     Input("bubble-color-metric", "value")]
)
def update_bubble_chart(year, reset_clicks, color_metric):
    if ctx.triggered_id == "reset-year-btn":
        filtered_df = ml_df[ml_df["State"] == "California"]
    else:
        filtered_df = ml_df[(ml_df["Year"] == year) & (ml_df["State"] == "California")]

    color_scale = "Reds" if color_metric == "FireCount" else "YlOrRd"

    fig = px.scatter(
        filtered_df,
        x="NDVI",
        y="DroughtSeverity",
        size="FireCount",
        color=color_metric,
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
            color_metric: "Fires Occurred" if color_metric == "FireCount" else color_metric
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
    # Use mean values if multiple rows
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


# Callback for linked line chart based on bubble chart selection and axis dropdown + info panel
@app.callback(
    [Output("linked-line-chart", "figure"),
     Output("info-panel", "children")],
    [Input("bubble-chart-california", "clickData"),
     Input("bubble-axis-selector", "value")]
)
def update_linked_line(clicked_point, axis_type):
    # If no point is selected, show a placeholder trend
    if not clicked_point:
        filtered = ml_df[ml_df["State"] == "California"]
        state = "California"
        year = None
    else:
        custom_data = clicked_point["points"][0].get("customdata", [])
        if len(custom_data) >= 2:
            state = custom_data[0]
            year = custom_data[1]
        else:
            state = "California"
            year = None
        filtered = ml_df[(ml_df["State"] == state)]

    if axis_type == "ndvi_drought":
        y_val = "DroughtSeverity"
        title = "Drought Severity Over Time"
        x_val = "Year"
    elif axis_type == "ndvi_temp":
        y_val = "NDVI"
        title = "NDVI Over Time"
        x_val = "Year"
    else:
        y_val = "FireCount"
        title = "FireCount Over Time"
        x_val = "Year"

    fig = px.line(filtered, x=x_val, y=y_val, title=title, markers=True)
    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        title_font=dict(family="Arial, sans-serif", size=22, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )

    # Info panel content
    info_text = "Select a bubble to see averages for that year."
    if year is not None:
        if isinstance(year, float) and not year.is_integer():
            info_text = f"Invalid year format detected: {year}."
            return fig, info_text
        year_data = ml_df[(ml_df["Year"] == year) & (ml_df["State"] == "California")]
        if not year_data.empty:
            avg_ndvi = year_data["NDVI"].mean()
            avg_firecount = year_data["FireCount"].mean()
            avg_temp = year_data["Temperature"].mean()
            info_text = f"Year {year} averages: NDVI = {avg_ndvi:.2f}, FireCount = {avg_firecount:.1f}, Temperature = {avg_temp:.1f}°F"
        else:
            info_text = f"No data available for year {year}."

    return fig, info_text



# Fire severity bubble chart timeline with dynamic color metric
@app.callback(
    Output("fire-severity-bubble", "figure"),
    [Input("active-tab", "data"),
     Input("bubble-axis-selector", "value"),
     Input("bubble-color-metric", "value")]
)
def update_fire_severity_timeline(tab, axis_type, color_metric):
    if tab != "correlations":
        return px.scatter()

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
    return fig


# Callback for Satellite Vegetation Comparison dropdown
@app.callback(
    Output("veg-map-display", "children"),
    Input("veg-map-year", "value")
)
def update_veg_maps(year):
    if year == "2001":
        return html.Div([
            html.Div([
                html.H4("California (2001)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/assets/2001_NVDI_CA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for California (2001)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2001-01-01", "2001-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "California")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2001");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"})
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("Georgia (2001)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/assets/2001_NVDI_GA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for Georgia (2001)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2001-01-01", "2001-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2001");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"})
            ])
        ])
    elif year == "2022":
        return html.Div([
            html.Div([
                html.H4("California (2022)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/assets/2022_NVDI_CA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for California (2022)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2022-01-01", "2022-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "California")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2022");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"})
            ], style={"marginBottom": "20px"}),
            html.Div([
                html.H4("Georgia (2022)", style={"textAlign": "center", "color": "#000000"}),
                html.Img(src="/assets/2022_NVDI_GA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                html.Pre("""// GEE NDVI for Georgia (2022)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2022-01-01", "2022-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2022");""",
                    style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"})
            ])
        ])
    else:  # Comparison view
        return html.Div([
            html.Div([
                html.H4("California: 2001 vs 2022", style={"textAlign": "center", "color": "#000000"}),
                html.Div([
                    html.Div([
                        html.Img(
                            src="/assets/2001_NVDI_CA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%", "marginRight": "2%"}),
                    html.Div([
                        html.Img(
                            src="/assets/2022_NVDI_CA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%"})
                ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "20px"})
            ]),
            html.Div([
                html.H4("Georgia: 2001 vs 2022", style={"textAlign": "center", "color": "#000000"}),
                html.Div([
                    html.Div([
                        html.Img(
                            src="/assets/2001_NVDI_GA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%", "marginRight": "2%"}),
                    html.Div([
                        html.Img(
                            src="/assets/2022_NVDI_GA_Map.png",
                            style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                        ),
                    ], style={"width": "49%"})
                ], style={"display": "flex", "justifyContent": "space-between"})
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