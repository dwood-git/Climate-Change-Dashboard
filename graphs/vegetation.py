"""Module for creating vegetation index graphs using Plotly.

This module provides functions to visualize vegetation trends over time.
- build_ndvi_graph: Visualizes the Normalized Difference Vegetation Index (NDVI) trends by state.
- build_evi_graph: Visualizes the Enhanced Vegetation Index (EVI) trends by state.

Last updated: May 2025
"""

import plotly.express as px

def build_ndvi_graph(df):
    """
    Builds a line graph showing NDVI trends over years for different states.

    Parameters:
    - df: DataFrame expected to have columns 'Year', 'NDVI', and 'State'.

    Returns:
    - A Plotly figure object visualizing NDVI trends.

    The graph uses distinct colors for each state and includes markers on data points.
    The layout includes a horizontally oriented legend below the graph.
    """
    fig = px.line(
        df,
        x='Year',  # X-axis represents years
        y='NDVI',  # Y-axis represents NDVI values
        color='State',  # Lines colored by state
        title=None,
        labels={'NDVI': 'Normalized Difference Vegetation Index', 'Year': 'Year'},
        markers=True  # Show markers on data points
    )
    # Customize hover information to show year, NDVI value formatted to 2 decimals, and state
    fig.update_traces(
        hovertemplate='Year: %{x}<br>NDVI: %{y:.2f}<br>State: %{customdata[0]}',
        customdata=df[['State']]  # Pass state information for hovertemplate
    )
    # Configure legend to be horizontal below the plot and set font styles
    fig.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'),
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )
    return fig

def build_evi_graph(df):
    """
    Builds a line graph showing EVI trends over years for different states.

    Parameters:
    - df: DataFrame expected to have columns 'Year', 'EVI', and 'State'.

    Returns:
    - A Plotly figure object visualizing EVI trends.

    The graph uses distinct colors for each state and includes markers on data points.
    The layout includes a horizontally oriented legend below the graph.
    """
    fig = px.line(
        df,
        x='Year',  # X-axis represents years
        y='EVI',  # Y-axis represents EVI values
        color='State',  # Lines colored by state
        title=None,
        labels={'EVI': 'Enhanced Vegetation Index', 'Year': 'Year'},
        markers=True  # Show markers on data points
    )
    # Customize hover information to show year, EVI value formatted to 2 decimals, and state
    fig.update_traces(
        hovertemplate='Year: %{x}<br>EVI: %{y:.2f}<br>State: %{customdata[0]}',
        customdata=df[['State']]  # Pass state information for hovertemplate
    )
    # Configure legend to be horizontal below the plot and set font styles
    fig.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'),
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )
    return fig
