"""Defines a reusable footer component for the Dash layout.

This module uses the Dash HTML components library to create a styled footer element
that can be included in the app's layout.

Last updated: May 2025
"""

from dash import html

def get_footer():
    """Returns a Dash HTML Footer component with project and data source information.

    The footer displays the author's name, data sources, and project year, styled with
    centered text, smaller font size, margin spacing, and a muted color.
    """
    # Render a footer element with project info and styling
    return html.Footer(
        "Built by Dylan Wood | Data sources: NASA, USGS, ERA5, USDM | Honors Project 2025",
        style={
            'textAlign': 'center',
            'fontSize': '13px',
            'marginTop': '40px',
            'marginBottom': '10px',
            'color': '#888'
        }
    )