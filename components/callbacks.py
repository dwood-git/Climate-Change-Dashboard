"""This module defines all Dash callback functions for interactivity within the app.
It manages user interactions for tabs, trends, vegetation, bubble charts, and correlations,
updating the corresponding components accordingly.

Last updated: May 2025
"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dash import Input, Output, State, dcc, html, ctx
import pandas as pd
import numpy as np
import plotly.express as px
from app import app, df_ga_filtered, df_precip_ga_filtered, df_ca_filtered, df_precip_ca_filtered, fig_ndvi_bubble
def render_tab_content(tab):
    """
    Renders the content for the selected tab.
    """
    if tab == "trends":
        return html.Div([
            html.Div([
                html.H4("Temperature Trends", className="graph-subtitle"),
                dcc.Graph(figure=fig_ga, config={"responsive": True}, style={"marginBottom": "40px"}),
                dcc.Graph(figure=fig_ca, config={"responsive": True})
            ]),
            html.Div([
                html.H4("Precipitation Trends", className="graph-subtitle"),
                dcc.Graph(figure=fig_precip_ga, config={"responsive": True}, style={"marginBottom": "40px"}),
                dcc.Graph(figure=fig_precip_ca, config={"responsive": True})
            ])
        ])
    elif tab == "veg":
        return html.Div([
            html.H4("NDVI vs EVI and Fire Count Bubble Chart", className="graph-subtitle"),
            dcc.Graph(
                id="ndvi-bubble-chart",
                figure=fig_ndvi_bubble,
                config={"responsive": True},
                style={"height": "650px", "margin": "auto"}
            ),
        ])
    elif tab == "correlations":
        return html.Div([
            html.H4("Correlation Visualizations Coming Soon...", className="graph-subtitle")
        ])
    else:
        return []
from graphs.correlations import create_bubble_chart, build_drought_line_graph, build_drought_heatmap, build_correlation_heatmap
from graphs.vegetation import build_ndvi_graph, build_evi_graph
from graphs.temperature import build_georgia_temperature_graph, build_california_temperature_graph
from graphs.precipitation import build_georgia_precip_graph, build_california_precip_graph

@app.callback(
    Output('active-tab', 'data'),
    [
        Input('btn-trends', 'n_clicks'),
        Input('btn-veg', 'n_clicks'),
        Input('btn-correlations', 'n_clicks'),
    ]
)
def update_tab(trends, veg, correlations):
    """
    Callback triggered by clicks on tab buttons (trends, vegetation, correlations).
    Uses the triggered button's id to determine which tab to activate.
    Returns the active tab identifier as a string.
    """
    trigger = ctx.triggered_id if ctx.triggered_id else "btn-trends"
    print("Click received. Triggered ID:", trigger)
    return trigger.replace('btn-', '')

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
    """
    Callback triggered by changes in bubble year dropdown, reset button clicks,
    or clicks on the drought line graph.
    Updates the stored selected year for the bubble chart.
    Returns the selected year or None if reset.
    """
    triggered = ctx.triggered_id
    if triggered == 'bubble-reset-btn':
        # Reset selection clears the stored year
        return None
    elif triggered == 'bubble-year-dropdown' and year_dropdown is not None:
        # Update store with year selected from dropdown
        return year_dropdown
    elif triggered == 'drought-line-graph' and drought_click is not None:
        # Update store with year clicked on drought line graph
        return drought_click['points'][0]['x']
    # If none of the above, retain current stored year
    return current_store

@app.callback(
    Output('bubble-chart', 'figure'),
    Input('bubble-year-store', 'data')
)
def update_bubble_chart_based_on_year(selected_year):
    """
    Callback triggered by changes to the stored selected bubble chart year.
    Filters the dataset for the selected year and generates a bubble chart.
    Returns the Plotly figure for the bubble chart.
    """
    ml_df = pd.read_csv('data/Fire_Model_California.csv')
    if selected_year is None:
        # If no year selected, show bubble chart for entire dataset
        return create_bubble_chart(ml_df)
    # Filter dataset to selected year; assume 'Year' column exists and is integer
    filtered_df = ml_df[ml_df['Year'] == int(selected_year)]
    if filtered_df.empty:
        # If filtered data is empty, fallback to full dataset chart
        return create_bubble_chart(ml_df)
    return create_bubble_chart(filtered_df)

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
    """
    Callback triggered by changes in start/end year dropdowns, reset button clicks,
    or trendline toggle selection.
    Filters temperature and precipitation datasets based on selected year range,
    then builds updated figures for Georgia and California temperature and precipitation graphs.
    Returns four Plotly figures corresponding to the graphs.
    """
    triggered = ctx.triggered_id if ctx.triggered_id else None

    # Copy filtered datasets to avoid modifying global dataframes
    dfg = df_ga_filtered.copy()
    dfgp = df_precip_ga_filtered.copy()
    dfc = df_ca_filtered.copy()
    dfcp = df_precip_ca_filtered.copy()

    if triggered == 'trends-reset-btn' or (start_year is None and end_year is None):
        # On reset or no year selection, use full datasets without filtering
        pass
    else:
        # Determine valid year range from Georgia dataset as baseline
        min_year = df_ga_filtered['Year'].min()
        max_year = df_ga_filtered['Year'].max()
        # Use selected years if provided, else default to min/max
        s_year = start_year if start_year is not None else min_year
        e_year = end_year if end_year is not None else max_year
        # Swap if start year is greater than end year to maintain logical range
        if s_year > e_year:
            s_year, e_year = e_year, s_year
        # Filter all datasets to the selected year range inclusively
        dfg = dfg[(dfg['Year'] >= s_year) & (dfg['Year'] <= e_year)]
        dfgp = dfgp[(dfgp['Year'] >= s_year) & (dfgp['Year'] <= e_year)]
        dfc = dfc[(dfc['Year'] >= s_year) & (dfc['Year'] <= e_year)]
        dfcp = dfcp[(dfcp['Year'] >= s_year) & (dfcp['Year'] <= e_year)]

    # Build figures using filtered or full datasets
    fig_ga_new = build_georgia_temperature_graph(dfg)
    fig_ca_new = build_california_temperature_graph(dfc)
    fig_precip_ga_new = build_georgia_precip_graph(dfgp)
    fig_precip_ca_new = build_california_precip_graph(dfcp)

    return fig_ga_new, fig_ca_new, fig_precip_ga_new, fig_precip_ca_new
@app.callback(
    Output('tab-content', 'children'),
    Input('active-tab', 'data')
)
def update_tab_content(tab):
    return render_tab_content(tab)
