from dash import Dash, html, dcc, Input, Output, ctx
import plotly.express as px
import pandas as pd
from graphs.temperature import build_georgia_temperature_graph, build_california_temperature_graph
from graphs.precipitation import build_georgia_precip_graph, build_california_precip_graph
from graphs.vegetation import build_ndvi_graph, build_evi_graph
from graphs.correlations import build_correlation_heatmap, build_drought_line_graph, build_drought_heatmap, build_bubble_chart
from loader import ClimateDataLoader

app = Dash(__name__)
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

veg_df = pd.read_csv("data/california/Fire_Model_California.csv")
fig_veg = html.Div([
    html.Div([
        html.H3("NDVI Line Chart", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_ndvi_graph(veg_df), config={'displayModeBar': False}),
            type="circle"
        ),
    ], className="graph-card")
], className="section-light")

drought_df = pd.read_csv("data/drought/Drought_Severity_California_Georgia.csv")
ml_df = pd.read_csv("data/california/Fire_Model_California.csv")

fig_corr = html.Div([
    html.Div([
        html.H3("Drought Severity Over Time", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_drought_line_graph(drought_df), config={'displayModeBar': False}),
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
        html.H3("NDVI, Drought, and Fires", className="graph-title"),
        dcc.Loading(
            dcc.Graph(figure=build_bubble_chart(ml_df), config={'displayModeBar': False}),
            type="circle"
        ),
    ], className="graph-card"),
], className="section-light")

app.layout = html.Div([
    html.H1("Wildfire Climate Change Visualization Dashboard", style={"textAlign": "center"}),
    html.P("Visualizing the relationship between climate change and wildfire patterns", style={"textAlign": "center"}),

    html.Div([
        html.Button("🌍 Historical Trends", id="btn-trends", n_clicks=0, className="nav-btn", style={'margin': '5px'}),
        html.Button("🌿 Vegetation Indices", id="btn-veg", n_clicks=0, className="nav-btn", style={'margin': '5px'}),
        html.Button("📈 Climate Correlations", id="btn-correlations", n_clicks=0, className="nav-btn", style={'margin': '5px'}),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'flexWrap': 'wrap',
        'gap': '10px',
        'margin': '20px auto'
    }),

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
    return trigger.replace("btn-", "")

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

if __name__ == "__main__":
    app.run_server(debug=True)
