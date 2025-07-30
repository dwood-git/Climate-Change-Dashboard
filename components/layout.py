"""
Defines the main layout for the Dash application.

This module uses Dash's HTML and core components to build the structure of the app,
including header, navigation buttons, data stores, dynamic content area, and footer.

Author: Dylan Wood
Last updated: January 2025
"""

from dash import html, dcc
from components.footer import get_footer


def get_main_layout():
    """
    Constructs and returns the main layout of the Dash application.

    The layout includes a header, navigation buttons for different views,
    hidden stores for managing state, a dynamic content area that updates
    based on user interaction, and a footer.

    Returns:
        html.Div: The root Div containing the entire app layout.
    """
    return html.Div([
        # Header section
        html.Div([
            html.H1("Wildfire Climate Change Visualization Dashboard", 
                    style={"textAlign": "center", "marginBottom": "10px"}),
            html.P("Visualizing the relationship between climate change and wildfire patterns", 
                   style={"textAlign": "center", "marginBottom": "30px"})
        ], className="header-section"),

        # Navigation buttons for switching between different dashboard views
        html.Div([
            html.Button("🌍 Historical Trends", id="btn-trends", n_clicks=0, className="nav-btn"),
            html.Button("🌿 Vegetation Indices", id="btn-veg", n_clicks=0, className="nav-btn"),
            html.Button("📈 Climate Correlations", id="btn-correlations", n_clicks=0, className="nav-btn"),
        ], className="nav-btn-container"),

        # Hidden stores to keep track of active tab and selected years for different visualizations
        dcc.Store(id='active-tab', data='trends'),
        dcc.Store(id='bubble-year-store', data=None),
        dcc.Store(id='trends-year-store', data=None),
        
        # Dynamic content area that updates based on the selected tab
        html.Div(id='tab-content', className="tab-content-container"),

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

        # Footer component at the bottom of the layout
        get_footer(),
    ])