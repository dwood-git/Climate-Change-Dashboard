"""
temperature.py

This module provides functions to visualize temperature trends for Georgia and California using Plotly Express and NumPy.
It includes scatter plots of average temperatures over years, trendlines, overall mean temperature lines, and 10-year moving averages.

Technologies used:
- Plotly Express for interactive plotting
- NumPy for polynomial fitting and numerical operations
"""

import numpy as np
import plotly.express as px

def build_georgia_temperature_graph(df):
    """
    Build a temperature trend graph for Georgia.

    Parameters:
    df (DataFrame): Must include columns 'Year' and 'AvgTemperature'.

    The graph includes:
    - Scatter points representing average temperature per year.
    - A green trendline showing the linear fit of temperature over years.
    - A red dashed line representing the overall average temperature.
    - An orange line showing the 10-year moving average of temperatures.

    Returns:
    fig (plotly.graph_objs._figure.Figure): The constructed Plotly figure object.
    """
    fig = px.scatter(df, x='Year', y='AvgTemperature', opacity=0.85)

    # Calculate linear trendline coefficients (slope and intercept)
    z = np.polyfit(df['Year'], df['AvgTemperature'], 1)
    trend = np.poly1d(z)
    # Add trendline to the figure
    fig.add_scatter(x=df['Year'], y=trend(df['Year']), mode='lines', name='Trendline', line=dict(color='green', width=2))

    # Calculate overall mean temperature
    mean = df['AvgTemperature'].mean()
    # Add mean temperature line
    fig.add_scatter(x=df['Year'], y=[mean]*len(df), mode='lines', name='Overall Avg', line=dict(color='red', dash='dash'))

    # Compute 10-year simple moving average (rolling mean)
    df['SMA_10'] = df['AvgTemperature'].rolling(window=10).mean()
    # Add moving average line
    fig.add_scatter(x=df['Year'], y=df['SMA_10'], mode='lines', name='10-Year Moving Avg', line=dict(color='orange'))

    # Customize hover info to show year and temperature with two decimals
    fig.update_traces(hovertemplate='Year: %{x}<br>Temperature: %{y:.2f}°F')
    # Update layout with axis titles, unified hovermode, and white template
    fig.update_layout(xaxis_title='Year', yaxis_title='Temperature (°F)', hovermode='x unified', template='plotly_white')

    return fig

def build_california_temperature_graph(df):
    """
    Build a temperature trend graph for California.

    Parameters:
    df (DataFrame): Must include columns 'Year' and 'AvgTemperature'.

    The graph includes:
    - Scatter points representing average temperature per year.
    - A green trendline showing the linear fit of temperature over years.
    - A red dashed line representing the overall average temperature.
    - An orange line showing the 10-year moving average of temperatures.

    Returns:
    fig (plotly.graph_objs._figure.Figure): The constructed Plotly figure object.
    """
    fig = px.scatter(df, x='Year', y='AvgTemperature', opacity=0.85)

    # Calculate linear trendline coefficients (slope and intercept)
    z = np.polyfit(df['Year'], df['AvgTemperature'], 1)
    trend = np.poly1d(z)
    # Add trendline to the figure
    fig.add_scatter(x=df['Year'], y=trend(df['Year']), mode='lines', name='Trendline', line=dict(color='green', width=2))

    # Calculate overall mean temperature
    mean = df['AvgTemperature'].mean()
    # Add mean temperature line
    fig.add_scatter(x=df['Year'], y=[mean]*len(df), mode='lines', name='Overall Avg', line=dict(color='red', dash='dash'))

    # Compute 10-year simple moving average (rolling mean)
    df['SMA_10'] = df['AvgTemperature'].rolling(window=10).mean()
    # Add moving average line
    fig.add_scatter(x=df['Year'], y=df['SMA_10'], mode='lines', name='10-Year Moving Avg', line=dict(color='orange'))

    # Customize hover info to show year and temperature with two decimals
    fig.update_traces(hovertemplate='Year: %{x}<br>Temperature: %{y:.2f}°F')
    # Update layout with axis titles, unified hovermode, and white template
    fig.update_layout(xaxis_title='Year', yaxis_title='Temperature (°F)', hovermode='x unified', template='plotly_white')

    return fig