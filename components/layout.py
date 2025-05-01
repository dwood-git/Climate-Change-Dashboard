"""Defines the main layout for the Dash application.

This module uses Dash's HTML and core components to build the structure of the app,
including header, navigation buttons, data stores, dynamic content area, and footer.

Last updated: May 2025
"""

from dash import html, dcc
from components.footer import get_footer

def get_main_layout():
    """Constructs and returns the main layout of the Dash application.

    The layout includes a header, navigation buttons for different views,
    hidden stores for managing state, a dynamic content area that updates
    based on user interaction, and a footer.

    Returns:
        html.Div: The root Div containing the entire app layout.
    """
    return html.Div([
        html.H1('Wildfire Climate Change Visualization Dashboard', style={'textAlign': 'center'}),
        html.P("Visualizing the relationship between climate change and wildfire patterns", style={'textAlign': 'center'}),
        
        # Navigation buttons for switching between different dashboard views
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
        
        # Hidden stores to keep track of active tab and selected years for different visualizations
        dcc.Store(id='active-tab', data='trends'),
        dcc.Store(id='bubble-year-store', data=None),
        dcc.Store(id='trends-year-store', data=None),
        
        # Dynamic content area that updates based on the selected tab
        html.Div(id='tab-content', children=[
            dcc.Graph(
                figure={
                    "data": [{"x": [1, 2, 3], "y": [4, 1, 2], "type": "scatter", "mode": "lines+markers"}],
                    "layout": {"title": "Test Graph: This should show if layout works"}
                }
            )
        ]),
        
        # Footer component at the bottom of the layout
        get_footer(),
    ])
