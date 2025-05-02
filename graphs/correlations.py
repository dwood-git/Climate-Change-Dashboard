"""Module for generating correlation-based visualizations related to drought, vegetation, and wildfire patterns.

This module uses Plotly Express and pandas to create interactive visualizations that help analyze
the relationships and trends among drought severity, vegetation indices, and wildfire occurrences.

Last updated: May 2025
"""

import plotly.express as px

def build_drought_line_graph(df):
    """
    Creates a line graph showing drought severity over time for different states.

    Parameters:
    df (pandas.DataFrame): DataFrame containing columns 'Year', 'DroughtSeverity', and 'State'.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive line graph figure.
    """
    # Line plot shows trends in drought severity by state over the years
    fig = px.line(
        df,
        x='Year',
        y='DroughtSeverity',
        color='State',
        title=None,
        labels={'DroughtSeverity': 'Drought Severity Index', 'Year': 'Year'},
        markers=True
    )
    # Customize legend orientation and font styles for clarity and aesthetics
    fig.update_layout(
        legend=dict(orientation='h', yanchor='bottom', y=-0.2, x=0.5, xanchor='center'),
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )
    return fig

def build_drought_heatmap(df):
    """
    Generates a heatmap visualizing drought severity across states and years.

    Parameters:
    df (pandas.DataFrame): DataFrame containing columns 'State', 'Year', and 'DroughtSeverity'.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive heatmap figure.
    """
    # Pivot the DataFrame to structure data with states as rows and years as columns
    drought_pivot = df.pivot(index='State', columns='Year', values='DroughtSeverity')
    # Heatmap communicates spatial-temporal variation in drought severity
    fig = px.imshow(
        drought_pivot,
        color_continuous_scale='YlOrRd',
        title=None,
        labels=dict(color="Drought Severity")
    )
    # Set font and title styling for readability
    fig.update_layout(
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )
    return fig

def build_correlation_heatmap(df):
    """
    Creates a heatmap of the correlation matrix among NDVI, EVI, Drought Severity, and Fire Count.

    Parameters:
    df (pandas.DataFrame): DataFrame containing columns 'NDVI', 'EVI', 'DroughtSeverity', and 'FireCount'.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive heatmap figure displaying correlation coefficients.
    """
    # Calculate correlation matrix for the selected variables
    corr_matrix = df[['NDVI', 'EVI', 'DroughtSeverity', 'FireCount']].corr()
    # Heatmap visualizes the strength and direction of correlations between variables
    fig = px.imshow(
        corr_matrix,
        text_auto=True,
        title=None,
        color_continuous_scale='RdBu',
        labels=dict(color="Correlation")
    )
    # Apply font and title styling for consistency and clarity
    fig.update_layout(
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )
    return fig

def build_bubble_chart(df):
    """
    Constructs a bubble chart showing the relationship between NDVI and drought severity,
    with bubble size and color representing fire occurrences.

    Parameters:
    df (pandas.DataFrame): DataFrame containing columns 'NDVI', 'DroughtSeverity', 'FireCount', and 'Year'.

    Returns:
    plotly.graph_objs._figure.Figure: An interactive scatter plot figure with bubbles.
    """
    # Scatter plot with bubble size and color encoding fire occurrence intensity
    fig_bubble = px.scatter(
        df,
        x='NDVI',
        y='DroughtSeverity',
        size='FireCount',
        color='FireCount',
        color_continuous_scale='YlOrRd',
        title=None,
        labels={
            'NDVI': 'NDVI (Vegetation Health)',
            'DroughtSeverity': 'Drought Severity Index',
            'FireCount': 'Fire Occurrence'
        },
        hover_data={
            'Year': True,
            'NDVI': ':.2f',
            'DroughtSeverity': ':.2f',
            'FireCount': True
        }
    )
    # Configure layout with axis ranges, grid styling, margins, and font settings for better visualization
    fig_bubble.update_layout(
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(title='NDVI (Vegetation Health)', range=[0.3, 0.6], showgrid=True, gridcolor='lightgray'),
        yaxis=dict(title='Drought Severity Index', range=[0.5, 4], showgrid=True, gridcolor='lightgray'),
        title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
        font=dict(family="Arial, sans-serif", color="#000000")
    )
    return fig_bubble