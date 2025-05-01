"""Module for visualizing precipitation trends for Georgia and California using scatter plots with trendlines.

This module provides functions to build precipitation graphs for Georgia and California based on input data.
It uses NumPy for polynomial fitting and Plotly Express for interactive plotting.

Libraries used:
- NumPy
- Plotly Express

Last updated: May 2025
"""

import numpy as np
import plotly.express as px

def build_georgia_precip_graph(df):
    """
    Builds a scatter plot with a trendline showing precipitation trends in Georgia.

    Parameters:
    - df: pandas DataFrame containing at least two columns:
        'Year' (int or float) representing the year,
        'AvgPrecip' (float) representing average precipitation in inches.

    The graph includes:
    - Scatter points representing yearly average precipitation.
    - A green trendline showing the linear fit of precipitation over years.

    Returns:
    - A Plotly Figure object with the precipitation scatter and trendline.
    """
    fig = px.scatter(df, x='Year', y='AvgPrecip', opacity=0.85)
    # Calculate the coefficients of a linear polynomial (degree 1) fit to the data
    z = np.polyfit(df['Year'], df['AvgPrecip'], 1)
    trend = np.poly1d(z)
    # Add a line trace representing the trendline based on the polynomial fit
    fig.add_scatter(x=df['Year'], y=trend(df['Year']), mode='lines', name='Trendline', line=dict(color='green', width=2))
    # Configure the layout with axis titles and a clean white template
    fig.update_layout(xaxis_title='Year', yaxis_title='Precipitation (inches)', template='plotly_white')
    return fig

def build_california_precip_graph(df):
    """
    Builds a scatter plot with a trendline showing precipitation trends in California.

    Parameters:
    - df: pandas DataFrame containing at least two columns:
        'Year' (int or float) representing the year,
        'AvgPrecip' (float) representing average precipitation in inches.

    The graph includes:
    - Scatter points representing yearly average precipitation.
    - A green trendline showing the linear fit of precipitation over years.

    Returns:
    - A Plotly Figure object with the precipitation scatter and trendline.
    """
    fig = px.scatter(df, x='Year', y='AvgPrecip', opacity=0.85)
    # Calculate the coefficients of a linear polynomial (degree 1) fit to the data
    z = np.polyfit(df['Year'], df['AvgPrecip'], 1)
    trend = np.poly1d(z)
    # Add a line trace representing the trendline based on the polynomial fit
    fig.add_scatter(x=df['Year'], y=trend(df['Year']), mode='lines', name='Trendline', line=dict(color='green', width=2))
    # Configure the layout with axis titles and a clean white template
    fig.update_layout(xaxis_title='Year', yaxis_title='Precipitation (inches)', template='plotly_white')
    return fig