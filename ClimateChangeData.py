"""
This project builds a Flask-Dash web app for visualizing the relationship between wildfire frequency, drought severity, vegetation health, and climate trends across Georgia and California.
"""

import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, send_from_directory, redirect
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import folium
import rasterio
import numpy as np
import matplotlib.colors as colors
from dash import ctx
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report


# =========================================================
# Data Loading and Cleaning
# =========================================================
"""Load and preprocess climate/precipitation data for Georgia and California."""
df_ga = pd.read_csv('data/GA_Yearly_Avg_Temps.csv', comment='#')
df_ga['Date'] = pd.to_datetime(df_ga['Date'], format='%Y%m')
df_ga['Year'] = df_ga['Date'].dt.year
df_ga['AvgTemperature'] = df_ga['Value']
# Filter Georgia data to 1980-2022
df_ga_filtered = df_ga[(df_ga['Year'] >= 1980) & (df_ga['Year'] <= 2022)]

# Load and clean the Georgia precipitation dataset
df_precip_ga = pd.read_csv('data/GA_Yearly_Avg_Precip.csv', comment='#')
df_precip_ga['Date'] = pd.to_datetime(df_precip_ga['Date'], format='%Y%m')
df_precip_ga['Year'] = df_precip_ga['Date'].dt.year
df_precip_ga['AvgPrecip'] = df_precip_ga['Value']
df_precip_ga_filtered = df_precip_ga[(df_precip_ga['Year'] >= 1980) & (df_precip_ga['Year'] <= 2022)]

# =========================================================
# Visualization Creation: Georgia Temperature
# =========================================================
"""Create Plotly figure for Georgia yearly average temperature, including trendline, overall average, and 10-year moving average."""
fig_ga = px.scatter(df_ga_filtered, x='Year', y='AvgTemperature',
              title=None,
              labels={'Year': 'Year', 'AvgTemperature': 'Temperature (°F)'},
              opacity=0.85)
# Trendline
z_ga = np.polyfit(df_ga_filtered['Year'], df_ga_filtered['AvgTemperature'], 1)
trend_ga = np.poly1d(z_ga)
fig_ga.add_scatter(x=df_ga_filtered['Year'], y=trend_ga(df_ga_filtered['Year']),
                mode='lines',
                name='Trendline',
                line=dict(color='green', width=2))
# Overall average
mean_temp_ga = df_ga_filtered['AvgTemperature'].mean()
fig_ga.add_scatter(x=df_ga_filtered['Year'], y=[mean_temp_ga]*len(df_ga_filtered),
                mode='lines',
                name='Overall Avg',
                line=dict(color='red', dash='dash'))
# 10-year moving average
df_ga_filtered['SMA_10'] = df_ga_filtered['AvgTemperature'].rolling(window=10).mean()
fig_ga.add_scatter(x=df_ga_filtered['Year'], y=df_ga_filtered['SMA_10'],
                mode='lines',
                name='10-Year Moving Avg',
                line=dict(color='orange'))
# Hovertemplate and style
fig_ga.update_traces(hovertemplate='Year: %{x}<br>Temperature: %{y:.2f}°F')
fig_ga.update_layout(
    title=None,
    xaxis_title='Year',
    yaxis_title='Temperature (°F)',
    hovermode='x unified',
    template='plotly_white',
    legend=dict(title='Legend', orientation='h', yanchor='bottom', y=-0.3, x=0.5, xanchor='center')
)
fig_ga.update_layout(
    title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
    font=dict(family="Arial, sans-serif", color="#000000")
)

# =========================================================
# Data Loading and Cleaning: California
# =========================================================
"""Load and preprocess climate/precipitation data for California."""
df_ca = pd.read_csv('data/CA_Yearly_Avg_Temps.csv', comment='#')
df_ca['Date'] = pd.to_datetime(df_ca['Date'], format='%Y%m')
df_ca['Year'] = df_ca['Date'].dt.year
df_ca['AvgTemperature'] = df_ca['Value']
# Filter California data to 1980-2022
df_ca_filtered = df_ca[(df_ca['Year'] >= 1980) & (df_ca['Year'] <= 2022)]

# Load and clean the California precipitation dataset
df_precip_ca = pd.read_csv('data/CA_Yearly_Avg_Precip.csv', comment='#')
df_precip_ca['Date'] = pd.to_datetime(df_precip_ca['Date'], format='%Y%m')
df_precip_ca['Year'] = df_precip_ca['Date'].dt.year
df_precip_ca['AvgPrecip'] = df_precip_ca['Value']
df_precip_ca_filtered = df_precip_ca[(df_precip_ca['Year'] >= 1980) & (df_precip_ca['Year'] <= 2022)]
# =========================================================
# Visualization Creation: Georgia/California Precipitation & California Temperature
# =========================================================
"""Create Plotly figures for precipitation and temperature trends for both states."""
#
## Georgia Precipitation graph (1980-2022)
fig_precip_ga = px.scatter(
    df_precip_ga_filtered,
    x='Year',
    y='AvgPrecip',
    labels={'Year': 'Year', 'AvgPrecip': 'Precipitation (inches)'},
    opacity=0.85
)
z_precip_ga = np.polyfit(df_precip_ga_filtered['Year'], df_precip_ga_filtered['AvgPrecip'], 1)
trend_precip_ga = np.poly1d(z_precip_ga)
fig_precip_ga.add_scatter(
    x=df_precip_ga_filtered['Year'],
    y=trend_precip_ga(df_precip_ga_filtered['Year']),
    mode='lines',
    name='Trendline',
    line=dict(color='green', width=2)
)

# California Precipitation graph (1980-2022)
fig_precip_ca = px.scatter(
    df_precip_ca_filtered,
    x='Year',
    y='AvgPrecip',
    labels={'Year': 'Year', 'AvgPrecip': 'Precipitation (inches)'},
    opacity=0.85
)
z_precip_ca = np.polyfit(df_precip_ca_filtered['Year'], df_precip_ca_filtered['AvgPrecip'], 1)
trend_precip_ca = np.poly1d(z_precip_ca)
fig_precip_ca.add_scatter(
    x=df_precip_ca_filtered['Year'],
    y=trend_precip_ca(df_precip_ca_filtered['Year']),
    mode='lines',
    name='Trendline',
    line=dict(color='green', width=2)
)

# California Avg Temperature graph (1980-2022)
fig_ca = px.scatter(df_ca_filtered, x='Year', y='AvgTemperature',
              title=None,
              labels={'Year': 'Year', 'AvgTemperature': 'Temperature (°F)'},
              opacity=0.85)
# Trendline
z_ca = np.polyfit(df_ca_filtered['Year'], df_ca_filtered['AvgTemperature'], 1)
trend_ca = np.poly1d(z_ca)
fig_ca.add_scatter(x=df_ca_filtered['Year'], y=trend_ca(df_ca_filtered['Year']),
                mode='lines',
                name='Trendline',
                line=dict(color='green', width=2))
# Overall average
mean_temp_ca = df_ca_filtered['AvgTemperature'].mean()
fig_ca.add_scatter(x=df_ca_filtered['Year'], y=[mean_temp_ca]*len(df_ca_filtered),
                mode='lines',
                name='Overall Avg',
                line=dict(color='red', dash='dash'))
# 10-year moving average
df_ca_filtered['SMA_10'] = df_ca_filtered['AvgTemperature'].rolling(window=10).mean()
fig_ca.add_scatter(x=df_ca_filtered['Year'], y=df_ca_filtered['SMA_10'],
                mode='lines',
                name='10-Year Moving Avg',
                line=dict(color='orange'))
# Hovertemplate and style
fig_ca.update_traces(hovertemplate='Year: %{x}<br>Temperature: %{y:.2f}°F')
fig_ca.update_layout(
    title=None,
    xaxis_title='Year',
    yaxis_title='Temperature (°F)',
    hovermode='x unified',
    template='plotly_white',
    legend=dict(title='Legend', orientation='h', yanchor='bottom', y=-0.3, x=0.5, xanchor='center')
)
fig_ca.update_layout(
    title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
    font=dict(family="Arial, sans-serif", color="#000000")
)

# Precipitation style updates
fig_precip_ga.update_layout(
    title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
    font=dict(family="Arial, sans-serif", color="#000000")
)
fig_precip_ca.update_layout(
    title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
    font=dict(family="Arial, sans-serif", color="#000000")
)

# =========================================================
# Wildfire Frequency Map Creation (Folium/Rasterio)
# =========================================================
"""Load California wildfire frequency raster, process, and overlay as a transparent PNG on a Folium map. Save as HTML for embedding."""
#
# Load the GeoTIFF
with rasterio.open("assets/California_FireFrequency_2001_2022.tif") as src:
    data = src.read(1)

# Plot and save as PNG with colormap
# Normalize and clean data
normed_data = data.astype(float)
normed_data[normed_data <= 0] = np.nan  # Mask zero and negative values
normed_data = normed_data / np.nanmax(normed_data)

# Plot colormap
plt.figure(figsize=(8, 10), dpi=300)  # adds clarity
plt.imshow(normed_data, cmap='gist_heat', interpolation='nearest', vmin=0, vmax=1)
plt.axis('off')

# Save as a transparent overlay
plt.savefig("assets/California_FireFrequency_Overlay.png", bbox_inches='tight', pad_inches=0, transparent=True)
plt.close()

# Generate the Folium wildfire map
wildfire_map = folium.Map(location=[36.5, -119], zoom_start=6)

folium.raster_layers.ImageOverlay(
    image='assets/California_FireFrequency_Overlay.png',
    bounds=[[32.0, -124.4], [42.1, -114.1]],  # CA bounds
    opacity=0.6,
    name='Fire Frequency'
).add_to(wildfire_map)

folium.LayerControl().add_to(wildfire_map)

# Save as an embeddable HTML file
wildfire_map.save("assets/california_fire_map.html")



# =========================================================
# Flask App Initialization and Routing
# =========================================================
"""Set up Flask server and static/homepage routing."""
server = Flask(__name__)

# Redirect from root to /home
@server.route("/")
def index():
    return redirect("/home")

# Flask Route for Homepage
@server.route("/home")
def landing_page():
    try:
        print("Serving landing.html from /home route")
        return send_from_directory('static', 'landing.html')
    except Exception as e:
        return f"<h1>Error loading landing page:</h1><p>{e}</p>", 500

# =========================================================
# Dash App Initialization and Layout
# =========================================================
"""Initialize Dash app, define navigation layout, and page structure."""
app = Dash(__name__, server=server, url_base_pathname="/dashboard/", suppress_callback_exceptions=True)

# Application Layout
app.layout = html.Div([
    html.H1('Wildfire Climate Change Visualization Dashboard', style={'textAlign': 'center'}),
    html.P("Visualizing the relationship between climate change and wildfire patterns", style={'textAlign': 'center'}),
    html.Div([
        html.Button("🌍 Historical Trends", id='btn-trends', n_clicks=0, className='nav-btn', style={'margin': '5px'}),
        html.Button("🌿 Vegetation Indices", id='btn-veg', n_clicks=0, className='nav-btn', style={'margin': '5px'}),
        html.Button("📈 Climate Correlations", id='btn-correlations', n_clicks=0, className='nav-btn', style={'margin': '5px'}),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'flexWrap': 'wrap',
        'gap': '10px',
        'margin': '20px auto'
    }),
    dcc.Store(id='active-tab', data='trends'),
    dcc.Store(id='bubble-year-store', data=None),
    dcc.Store(id='trends-year-store', data=None),
    html.Div(id='tab-content'),
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

# =========================================================
# Dash Callback Functions
# =========================================================
"""Dash callbacks for tab navigation, bubble chart interactivity, and content rendering."""

@app.callback(
    Output('active-tab', 'data'),
    [
        Input('btn-trends', 'n_clicks'),
        Input('btn-veg', 'n_clicks'),
        Input('btn-correlations', 'n_clicks'),
    ],
    prevent_initial_call=True
)
def update_tab(trends, veg, correlations):
    # Switch tabs based on which navigation button was clicked
    if not ctx.triggered:
        return ctx.no_update
    return ctx.triggered_id.replace('btn-', '')

# Bubble Chart Interactivity: Dropdown, Reset, and click on drought line
@app.callback(
    Output('bubble-year-store', 'data'),
    [
        Input('bubble-year-dropdown', 'value'),
        Input('bubble-reset-btn', 'n_clicks'),
        Input('drought-line-graph', 'clickData')
    ],
    State('bubble-year-store', 'data')
)
def update_bubble_year_store(year_dropdown, reset_clicks, drought_click, current_store):
    # Determine which input triggered the callback
    triggered = ctx.triggered_id
    if triggered == 'bubble-reset-btn':
        # Reset to all years if reset button pressed
        return None
    elif triggered == 'bubble-year-dropdown' and year_dropdown is not None:
        # Filter by selected year from dropdown
        return year_dropdown
    elif triggered == 'drought-line-graph' and drought_click is not None:
        # Set year based on clicked point in drought line graph
        return drought_click['points'][0]['x']
    return current_store

@app.callback(
    Output('bubble-chart', 'figure'),
    Input('bubble-year-store', 'data')
)
def update_bubble_chart_based_on_year(selected_year):
    import pandas as pd
    import plotly.express as px
    ml_df = pd.read_csv('data/Fire_Model_California_Georgia.csv')
    def create_bubble_chart(df):
        fig_bubble = px.scatter(
            df,
            x='NDVI',
            y='DroughtSeverity',
            size='Fire',
            color='State',
            title=None,
            labels={
                'NDVI': 'NDVI (Vegetation Health)',
                'DroughtSeverity': 'Drought Severity Index',
                'Fire': 'Fire Occurrence'
            },
            hover_data=['Year']
        )
        fig_bubble.update_layout(
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(title='NDVI (Vegetation Health)', range=[0.2, 1.0]),
            yaxis=dict(title='Drought Severity Index', range=[0, 4]),
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )
        return fig_bubble
    # Show all years if no year selected, otherwise filter to selected year
    if selected_year is None:
        return create_bubble_chart(ml_df)
    filtered_df = ml_df[ml_df['Year'] == int(selected_year)]
    if filtered_df.empty:
        return create_bubble_chart(ml_df)
    return create_bubble_chart(filtered_df)

@app.callback(
    Output('tab-content', 'children'),
    Input('active-tab', 'data')
)
def render_tab_content(tab):
    if tab == 'trends':
        # --------------------------
        # Trends Tab Content
        # --------------------------
        # Years for dropdowns
        years = sorted(df_ga_filtered['Year'].unique())
        start_year_dropdown = dcc.Dropdown(
            id='start-year-dropdown',
            options=[{'label': str(y), 'value': y} for y in years],
            placeholder="Start Year",
            style={'width': '120px', 'margin': '0 5px'},
            clearable=True,
        )
        end_year_dropdown = dcc.Dropdown(
            id='end-year-dropdown',
            options=[{'label': str(y), 'value': y} for y in years],
            placeholder="End Year",
            style={'width': '120px', 'margin': '0 5px'},
            clearable=True,
        )
        trends_reset_btn = html.Button(
            "Reset to All Years",
            id='trends-reset-btn',
            n_clicks=0,
            style={
                'margin': '0 10px',
                'backgroundColor': '#e0e0e0',
                'color': '#222',
                'fontFamily': 'Arial, sans-serif',
                'borderRadius': '8px',
                'border': '1px solid #bbb',
                'padding': '6px 20px',
                'fontWeight': 'bold'
            }
        )
        trendline_toggle = dcc.RadioItems(
            id='trendline-toggle',
            options=[
                {'label': 'Show Trendlines', 'value': 'show'},
                {'label': 'Hide Trendlines', 'value': 'hide'}
            ],
            value='show',
            inline=True,
            style={'margin': '0 10px'}
        )
        controls_row = html.Div(
            [
                start_year_dropdown,
                end_year_dropdown,
                trendline_toggle,
                trends_reset_btn
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'marginBottom': '25px',
                'gap': '10px',
                'flexWrap': 'wrap'
            }
        )
        return html.Div([
            html.H2(
                "🌍 Historical Trends",
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#FFFFFF',
                    'fontSize': '32px'
                }
            ),
            html.P(
                "Visualizing yearly average temperatures and climate trends (1980–2022) for Georgia and California.",
                style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#FFFFFF',
                    'fontSize': '18px'
                }
            ),
            html.Div([
                controls_row,
                dcc.Loading(
                    type="circle",
                    color="#3b6ea5",
                    children=[
                        html.H3(
                            "Georgia Yearly Average Temperature",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '26px'
                            }
                        ),
                        dcc.Graph(id='ga-temp-graph', figure=fig_ga, config={'displayModeBar': False}, style={'marginBottom': '10px'}),
                        html.P(
                            "Georgia's average annual temperature from 1980 to 2022 shows a gradual warming trend, with year-to-year variability and a notable upward slope.",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '16px',
                                'fontStyle': 'italic',
                                'marginBottom': '30px'
                            }
                        ),
                        html.H3(
                            "California Yearly Average Temperature",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '26px',
                                'marginTop': '40px'
                            }
                        ),
                        dcc.Graph(id='ca-temp-graph', figure=fig_ca, config={'displayModeBar': False}, style={'marginBottom': '10px'}),
                        html.P(
                            "California's average annual temperature over the same period also reveals a warming trend, with more pronounced fluctuations and a clear increase in recent decades.",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '16px',
                                'fontStyle': 'italic',
                                'marginBottom': '30px'
                            }
                        ),
                        html.H2(
                            "🌧️ Annual Precipitation Trends (1980–2022)",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '32px',
                                'marginTop': '40px'
                            }
                        ),
                        html.P(
                            "Visualizing yearly average precipitation trends (1980–2022) for Georgia and California.",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '18px'
                            }
                        ),
                        html.H3(
                            "Georgia Yearly Average Precipitation",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '26px'
                            }
                        ),
                        dcc.Graph(id='ga-precip-graph', figure=fig_precip_ga, config={'displayModeBar': False}, style={'marginBottom': '10px'}),
                        html.P(
                            "Georgia's annual precipitation exhibits variability but no strong long-term trend, reflecting the state's relatively stable rainfall patterns.",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '16px',
                                'fontStyle': 'italic',
                                'marginBottom': '30px'
                            }
                        ),
                        html.H3(
                            "California Yearly Average Precipitation",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '26px',
                                'marginTop': '40px'
                            }
                        ),
                        dcc.Graph(id='ca-precip-graph', figure=fig_precip_ca, config={'displayModeBar': False}, style={'marginBottom': '10px'}),
                        html.P(
                            "California's precipitation is highly variable, with periods of drought and wet years, contributing to wildfire risk and ecosystem stress.",
                            style={
                                'textAlign': 'center',
                                'fontFamily': 'Arial, sans-serif',
                                'color': '#000000',
                                'fontSize': '16px',
                                'fontStyle': 'italic',
                                'marginBottom': '30px'
                            }
                        ),
                        html.P([
                            "Data Source: ",
                            html.A("NOAA National Centers for Environmental Information (NCEI)",
                                href="https://www.ncei.noaa.gov/",
                                target="_blank",
                                style={'color': 'blue', 'textDecoration': 'underline'})
                        ], style={
                            'textAlign': 'center',
                            'fontFamily': 'Arial, sans-serif',
                            'color': '#000000',
                            'fontSize': '16px',
                            'fontStyle': 'italic',
                            'marginTop': '10px'
                        })
                    ]
                )
            ], style={
                'backgroundColor': '#f8f8f8',
                'padding': '30px 15px',
                'margin': '30px auto',
                'borderRadius': '16px',
                'maxWidth': '950px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.03)'
            })
        ])
    elif tab == 'veg':
        # --------------------------
        # Vegetation Indices Tab Content
        # --------------------------
        veg_df = pd.read_csv('data/Vegetation_Index_California_Georgia.csv')

        fig_ndvi = px.line(
            veg_df,
            x='Year',
            y='NDVI',
            color='State',
            title=None,
            labels={'NDVI': 'Normalized Difference Vegetation Index', 'Year': 'Year'},
            markers=True
        )
        fig_ndvi.update_traces(
            hovertemplate='Year: %{x}<br>NDVI: %{y:.2f}<br>State: %{customdata[0]}',
            customdata=veg_df[['State']]
        )
        fig_ndvi.update_layout(legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'))
        fig_ndvi.update_layout(
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )

        fig_evi = px.line(
            veg_df,
            x='Year',
            y='EVI',
            color='State',
            title=None,
            labels={'EVI': 'Enhanced Vegetation Index', 'Year': 'Year'},
            markers=True
        )
        fig_evi.update_traces(
            hovertemplate='Year: %{x}<br>EVI: %{y:.2f}<br>State: %{customdata[0]}',
            customdata=veg_df[['State']]
        )
        fig_evi.update_layout(legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'))
        fig_evi.update_layout(
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )

        return html.Div([
            html.H2("🌿 Vegetation Indices", style={'textAlign': 'center'}),
            html.P("Comparison of vegetation health indicators (NDVI and EVI) between California and Georgia from 2001 to 2020.", style={'textAlign': 'center'}),
            html.Div([
                html.H3(
                    "NDVI Over Time: California vs Georgia",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px'
                    }
                ),
                dcc.Graph(figure=fig_ndvi, style={'marginBottom': '10px'}),
                html.P(
                    "NDVI (Normalized Difference Vegetation Index) reflects the greenness and density of vegetation; higher values indicate healthier plant cover.",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '16px',
                        'fontStyle': 'italic',
                        'marginBottom': '30px'
                    }
                ),
                html.H3(
                    "EVI Over Time: California vs Georgia",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px',
                        'marginTop': '35px'
                    }
                ),
                dcc.Graph(figure=fig_evi, style={'marginBottom': '10px'}),
                html.P(
                    "EVI (Enhanced Vegetation Index) provides an alternative measure of vegetation health, less sensitive to atmospheric effects and dense canopies.",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '16px',
                        'fontStyle': 'italic',
                        'marginBottom': '30px'
                    }
                ),
                html.P([
                    "Dataset Source: ",
                    html.A("NASA MODIS Vegetation Indices (MOD13A2 v6.1)",
                        href="https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A2",
                        target="_blank",
                        style={'color': 'blue', 'textDecoration': 'underline'})
                ], style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#000000',
                    'fontSize': '16px',
                    'fontStyle': 'italic',
                    'marginTop': '10px'
                })
            ], style={
                'backgroundColor': '#f8f8f8',
                'padding': '30px 15px',
                'margin': '30px auto',
                'borderRadius': '16px',
                'maxWidth': '950px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.03)'
            })
        ])
    elif tab == 'correlations':
        # --------------------------
        # Climate Correlations Tab Content
        # --------------------------
        drought_df = pd.read_csv('data/Drought_Severity_California_Georgia.csv')
        ml_df = pd.read_csv('data/Fire_Model_California_Georgia.csv')

        # Create Drought Severity Line Graph
        fig_drought = px.line(
            drought_df,
            x='Year',
            y='DroughtSeverity',
            color='State',
            title=None,
            labels={'DroughtSeverity': 'Drought Severity Index', 'Year': 'Year'},
            markers=True
        )
        fig_drought.update_layout(legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'))
        fig_drought.update_layout(
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )

        # Create Drought Severity Heatmap
        drought_pivot = drought_df.pivot(index='State', columns='Year', values='DroughtSeverity')
        fig_drought_heatmap = px.imshow(
            drought_pivot,
            color_continuous_scale='YlOrRd',
            title=None,
            labels=dict(color="Drought Severity")
        )
        fig_drought_heatmap.update_layout(
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )

        # Correlation Heatmap
        corr_matrix = ml_df[['NDVI', 'EVI', 'DroughtSeverity', 'Fire']].corr()
        fig_corr_heatmap = px.imshow(
            corr_matrix,
            text_auto=True,
            title=None,
            color_continuous_scale='RdBu',
            labels=dict(color="Correlation")
        )
        fig_corr_heatmap.update_layout(
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )

        # Bubble chart year dropdown and reset
        bubble_years = sorted(ml_df['Year'].unique())
        bubble_dropdown = dcc.Dropdown(
            id='bubble-year-dropdown',
            options=[{'label': str(y), 'value': y} for y in bubble_years],
            placeholder="Filter by Year...",
            style={'width': '200px', 'margin': '0 10px'},
            clearable=True,
        )
        bubble_reset_btn = html.Button(
            "Reset to All Years",
            id='bubble-reset-btn',
            n_clicks=0,
            style={
                'margin': '0 10px',
                'backgroundColor': '#e0e0e0',
                'color': '#222',
                'fontFamily': 'Arial, sans-serif',
                'borderRadius': '8px',
                'border': '1px solid #bbb',
                'padding': '6px 20px',
                'fontWeight': 'bold'
            }
        )
        bubble_controls_row = html.Div(
            [
                bubble_dropdown,
                bubble_reset_btn
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'marginBottom': '25px',
                'gap': '10px'
            }
        )
        return html.Div([
            html.H2("📈 Climate Correlations", style={'textAlign': 'center'}),
            html.P(
                "This section explores how environmental factors such as drought severity and vegetation health relate to wildfire occurrence.",
                style={'textAlign': 'center', 'marginBottom': '20px'}
            ),
            html.Div([
                html.H3(
                    "Drought Severity Over Time: California vs Georgia",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px'
                    }
                ),
                dcc.Graph(id='drought-line-graph', figure=fig_drought, style={'marginBottom': '10px'}),
                html.P(
                    "Drought severity indices show how water scarcity fluctuates annually, impacting vegetation and fire risk.",
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
                html.P([
                    "Drought Dataset Source: ",
                    html.A("US Drought Monitor (USDM)", href="https://droughtmonitor.unl.edu/", target="_blank", style={'color': 'blue', 'textDecoration': 'underline'})
                ], style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#000000',
                    'fontSize': '16px',
                    'fontStyle': 'italic',
                    'marginTop': '10px',
                    'marginBottom': '30px'
                }),

                html.H3(
                    "Drought Severity Heatmap",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px'
                    }
                ),
                dcc.Graph(figure=fig_drought_heatmap, style={'marginBottom': '10px'}),
                html.P(
                    "Heatmap visualization highlights the intensity and variation in drought conditions by state and year.",
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

                html.H3(
                    "Feature Correlation Matrix",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px'
                    }
                ),
                dcc.Graph(figure=fig_corr_heatmap, style={'marginBottom': '10px'}),
                html.P([
                    "Vegetation Indices Source: ",
                    html.A("NASA MODIS Vegetation Indices (MOD13A2 v6.1)", href="https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MOD13A2", target="_blank", style={'color': 'blue', 'textDecoration': 'underline'})
                ], style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#000000',
                    'fontSize': '16px',
                    'fontStyle': 'italic',
                    'marginTop': '10px',
                    'marginBottom': '30px'
                }),

                html.H3(
                    "Vegetation Health vs Drought Severity vs Fire Occurrence",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px'
                    }
                ),
                bubble_controls_row,
                dcc.Loading(
                    type="circle",
                    color="#3b6ea5",
                    children=[
                        dcc.Graph(id='bubble-chart', style={'marginBottom': '10px'})
                    ]
                ),
                html.P(
                    "Bubble chart relates NDVI and drought severity to fire occurrence; larger bubbles indicate more fires.",
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
                html.H3(
                    "California Wildfire Frequency Map (2001–2022)",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px'
                    }
                ),
                html.Iframe(
                    srcDoc=open('assets/california_fire_map.html', 'r').read(),
                    width='100%',
                    height='600',
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
                ),
                html.P([
                    "California Fire Frequency Data Source: ",
                    html.A("NASA MODIS Burned Area Product (MCD64A1 v6)", href="https://developers.google.com/earth-engine/datasets/catalog/MODIS_006_MCD64A1", target="_blank", style={'color': 'blue', 'textDecoration': 'underline'})
                ], style={
                    'textAlign': 'center',
                    'fontFamily': 'Arial, sans-serif',
                    'color': '#000000',
                    'fontSize': '16px',
                    'fontStyle': 'italic',
                    'marginTop': '10px'
                }),
                html.H3(
                    "Georgia Wildfire Frequency Map (2001–2022)",
                    style={
                        'textAlign': 'center',
                        'fontFamily': 'Arial, sans-serif',
                        'color': '#000000',
                        'fontSize': '26px',
                        'marginTop': '50px'
                    }
                ),
                html.Img(
                    src="/dashboard/assets/ga_firefreq_map.jpg",
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
                ),
                html.P(
                    "🔥 Dynamic Georgia wildfire analysis coming soon!",
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
                # --- End Regional Impact Section ---
            ], style={
                'backgroundColor': '#f8f8f8',
                'padding': '30px 15px',
                'margin': '30px auto',
                'borderRadius': '16px',
                'maxWidth': '950px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.03)'
            })
        ])


    else:
        return html.Div(f"{tab.capitalize()} section coming soon...", style={'textAlign': 'center', 'marginTop': '50px'})

# =========================================================
# Run the Integrated App
# =========================================================
"""Start the Flask server if the script is run directly."""
if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5050")
    server.run(debug=True, port=5050)

# =========================================================
# Trends Graphs Filtering Callback (Year Range)
# =========================================================
"""Dash callback for filtering all four trend graphs based on year range and trendline toggle."""
# Filtering callback for all 4 graphs (GA/CA temp/precip) with year range
@app.callback(
    Output('ga-temp-graph', 'figure'),
    Output('ca-temp-graph', 'figure'),
    Output('ga-precip-graph', 'figure'),
    Output('ca-precip-graph', 'figure'),
    [
        Input('start-year-dropdown', 'value'),
        Input('end-year-dropdown', 'value'),
        Input('trends-reset-btn', 'n_clicks'),
        Input('trendline-toggle', 'value')
    ]
)
def update_trends_graphs(start_year, end_year, reset_clicks, trendline_toggle):
    # Use dash.ctx (Dash 2.4+) to determine which input triggered the callback
    triggered = ctx.triggered_id if ctx.triggered_id else None

    # Start with full filtered dataframes
    dfg = df_ga_filtered.copy()
    dfgp = df_precip_ga_filtered.copy()
    dfc = df_ca_filtered.copy()
    dfcp = df_precip_ca_filtered.copy()

    if triggered == 'trends-reset-btn' or (start_year is None and end_year is None):
        # Reset: Show full range
        pass
    else:
        # Filter by selected year range
        min_year = df_ga_filtered['Year'].min()
        max_year = df_ga_filtered['Year'].max()
        s_year = start_year if start_year is not None else min_year
        e_year = end_year if end_year is not None else max_year
        if s_year > e_year:
            s_year, e_year = e_year, s_year
        dfg = dfg[(dfg['Year'] >= s_year) & (dfg['Year'] <= e_year)]
        dfgp = dfgp[(dfgp['Year'] >= s_year) & (dfgp['Year'] <= e_year)]
        dfc = dfc[(dfc['Year'] >= s_year) & (dfc['Year'] <= e_year)]
        dfcp = dfcp[(dfcp['Year'] >= s_year) & (dfcp['Year'] <= e_year)]

    # Georgia Temp Graph
    fig_ga_new = px.scatter(dfg, x='Year', y='AvgTemperature', title=None,
                            labels={'Year': 'Year', 'AvgTemperature': 'Temperature (°F)'}, opacity=0.85)
    if trendline_toggle == 'show' and len(dfg) >= 2:
        z = np.polyfit(dfg['Year'], dfg['AvgTemperature'], 1)
        fig_ga_new.add_traces([
            px.line(x=dfg['Year'], y=np.poly1d(z)(dfg['Year'])).data[0]
        ])
    fig_ga_new.update_layout(template='plotly_white', hovermode='x unified')

    # California Temp Graph
    fig_ca_new = px.scatter(dfc, x='Year', y='AvgTemperature', title=None,
                            labels={'Year': 'Year', 'AvgTemperature': 'Temperature (°F)'}, opacity=0.85)
    if trendline_toggle == 'show' and len(dfc) >= 2:
        z = np.polyfit(dfc['Year'], dfc['AvgTemperature'], 1)
        fig_ca_new.add_traces([
            px.line(x=dfc['Year'], y=np.poly1d(z)(dfc['Year'])).data[0]
        ])
    fig_ca_new.update_layout(template='plotly_white', hovermode='x unified')

    # Georgia Precipitation Graph
    fig_precip_ga_new = px.scatter(dfgp, x='Year', y='AvgPrecip', title=None,
                                   labels={'Year': 'Year', 'AvgPrecip': 'Precipitation (inches)'}, opacity=0.85)
    if trendline_toggle == 'show' and len(dfgp) >= 2:
        z = np.polyfit(dfgp['Year'], dfgp['AvgPrecip'], 1)
        fig_precip_ga_new.add_traces([
            px.line(x=dfgp['Year'], y=np.poly1d(z)(dfgp['Year'])).data[0]
        ])
    fig_precip_ga_new.update_layout(template='plotly_white', hovermode='x unified')

    # California Precipitation Graph
    fig_precip_ca_new = px.scatter(dfcp, x='Year', y='AvgPrecip', title=None,
                                   labels={'Year': 'Year', 'AvgPrecip': 'Precipitation (inches)'}, opacity=0.85)
    if trendline_toggle == 'show' and len(dfcp) >= 2:
        z = np.polyfit(dfcp['Year'], dfcp['AvgPrecip'], 1)
        fig_precip_ca_new.add_traces([
            px.line(x=dfcp['Year'], y=np.poly1d(z)(dfcp['Year'])).data[0]
        ])
    fig_precip_ca_new.update_layout(template='plotly_white', hovermode='x unified')

    return fig_ga_new, fig_ca_new, fig_precip_ga_new, fig_precip_ca_new
