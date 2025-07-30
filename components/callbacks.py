"""
Callback functions for the Dash application.

This module contains all the callback functions that handle user interactions
and update the dashboard components accordingly. It manages tab switching,
data filtering, and dynamic content updates.

Author: Dylan Wood
Last updated: January 2025
"""

from dash import Input, Output, State, ctx, exceptions
import plotly.express as px
import pandas as pd
from components.dashboard_components import (
    create_historical_trends_section,
    create_vegetation_section,
    create_correlations_section
)


def register_callbacks(app, data_manager):
    """
    Register all callback functions with the Dash application.
    
    Args:
        app: Dash application instance
        data_manager: DataManager instance containing all datasets
    """
    
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
        return trigger.replace("btn-", "") if trigger.startswith("btn-") else "trends"

    @app.callback(
        Output("tab-content", "children"),
        Input("active-tab", "data")
    )
    def render_tab(tab):
        """
        Render the appropriate content based on the selected tab.
        
        Args:
            tab: String identifier for the active tab
            
        Returns:
            html.Div: The content component for the selected tab
        """
        if tab == "trends":
            return create_historical_trends_section(data_manager)
        elif tab == "veg":
            return create_vegetation_section(data_manager)
        elif tab == "correlations":
            return create_correlations_section(data_manager)
        return html.Div("Select a view above.")

    # Callback for California-only bubble chart with year slider and reset button + Fire Risk Badge update
    @app.callback(
        [Output("bubble-chart-california", "figure"),
         Output("fire-risk-badge", "children")],
        [Input("year-slider", "value"),
         Input("reset-year-btn", "n_clicks")]
    )
    def update_bubble_chart(year, reset_clicks):
        """
        Update the California bubble chart based on year selection and reset button.
        
        Args:
            year: Selected year from slider
            reset_clicks: Number of clicks on reset button
            
        Returns:
            tuple: (figure, risk_text) - Updated bubble chart and risk assessment
        """
        color_metric = "FireCount"
        ca_df = data_manager.get_california_fire_data()
        
        if ctx.triggered_id == "reset-year-btn":
            filtered_df = ca_df
        else:
            filtered_df = ca_df[ca_df["Year"] == year] if year else ca_df

        fig = px.scatter(
            filtered_df,
            x="NDVI",
            y="DroughtSeverity",
            size="FireCount",
            color="FireCount",
            color_continuous_scale=[
                "#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C", "#FD8D3C",
                "#FC4E2A", "#E31A1C", "#BD0026", "#800026"
            ],
            hover_data=["Year", "State"],
            title=None,
            labels={
                "NDVI": "NDVI (Vegetation Health)",
                "DroughtSeverity": "Drought Severity Index",
                "FireCount": "Fires Occurred",
                "Temperature": "Temperature (°F)",
                "FireCount": "Fires Occurred"
            }
        )
        fig.update_layout(
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(title='NDVI (Vegetation Health)', range=[0.2, 1.0]),
            yaxis=dict(title='Drought Severity Index', range=[0, 4]),
            title_font=dict(family="Arial, sans-serif", size=24, color="#000000"),
            font=dict(family="Arial, sans-serif", color="#000000")
        )

        # Fire Risk Badge logic
        risk_text = ""
        drought_mean = filtered_df["DroughtSeverity"].mean() if not filtered_df.empty else 0
        ndvi_mean = filtered_df["NDVI"].mean() if not filtered_df.empty else 1
        firecount_mean = filtered_df["FireCount"].mean() if not filtered_df.empty else 0

        if (drought_mean > 2.5) and (ndvi_mean < 0.38) and (firecount_mean > 400):
            risk_text = "🔥 High Risk"
        elif (drought_mean > 1.5) and (ndvi_mean < 0.5) and (firecount_mean > 200):
            risk_text = "⚠️ Moderate Risk"
        else:
            risk_text = "✅ Low Risk"

        return fig, risk_text

    # Callback for linked bubble timeline chart: always show full CA data, info panel static
    @app.callback(
        [Output("fire-severity-bubble", "figure"),
         Output("info-panel", "children")],
        [Input("bubble-chart-california", "clickData")]
    )
    def update_linked_line(_):
        """
        Update the fire severity bubble timeline chart.
        
        Args:
            _: Click data from bubble chart (unused)
            
        Returns:
            tuple: (figure, info_text) - Updated timeline chart and info panel
        """
        df = data_manager.get_california_fire_data()
        fig = px.scatter(
            df,
            x="Year",
            y="DroughtSeverity",
            size="FireCount",
            color="NDVI",
            color_continuous_scale="YlGn",
            hover_data=["FireCount", "NDVI"],
            labels={
                "Year": "Year",
                "DroughtSeverity": "Drought Index",
                "FireCount": "Fires",
                "NDVI": "NDVI (Vegetation Health)"
            }
        )
        fig.update_layout(
            margin=dict(l=40, r=40, t=40, b=40),
            title_font=dict(family="Arial, sans-serif", size=22),
            font=dict(family="Arial, sans-serif")
        )
        return fig, "Click on any bubble in the chart above to see detailed information."

    # Callback for Satellite Vegetation Comparison dropdown
    @app.callback(
        Output("veg-map-display", "children"),
        Input("veg-map-year", "value")
    )
    def update_veg_maps(year):
        """
        Update the vegetation map display based on year selection.
        
        Args:
            year: Selected year ('2001', '2022', or 'compare')
            
        Returns:
            html.Div: Vegetation map display component
        """
        from dash import html
        
        if year == "2001":
            return html.Div([
                # Accessible, text-based NDVI color legend
                html.Div([
                    html.H4("NDVI Color Key", style={"textAlign": "center", "color": "#000000", "marginBottom": "10px"}),
                    html.P("🟩 Green: Healthy/Dense Vegetation (NDVI > 0.6)", style={"textAlign": "center", "margin": "2px", "color": "#006400"}),
                    html.P("🟨 Yellow: Moderate Vegetation (NDVI ≈ 0.4–0.6)", style={"textAlign": "center", "margin": "2px", "color": "#DAA520"}),
                    html.P("⬜ White: Low or No Vegetation (NDVI < 0.2)", style={"textAlign": "center", "margin": "2px", "color": "#555555"}),
                ], style={"marginBottom": "20px"}),
                html.Div([
                    html.H4("California (2001)", style={"textAlign": "center", "color": "#000000"}),
                    html.Img(src="/static/2001_NVDI_CA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                    html.Pre("""// GEE NDVI for California (2001)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2001-01-01", "2001-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "California")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2001");""",
                        style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                    html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
                ], style={"marginBottom": "20px"}),
                html.Div([
                    html.H4("Georgia (2001)", style={"textAlign": "center", "color": "#000000"}),
                    html.Img(src="/static/2001_NVDI_GA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                    html.Pre("""// GEE NDVI for Georgia (2001)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2001-01-01", "2001-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2001");""",
                        style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                    html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
                ])
            ])
        elif year == "2022":
            return html.Div([
                # Accessible, text-based NDVI color legend
                html.Div([
                    html.H4("NDVI Color Key", style={"textAlign": "center", "color": "#000000", "marginBottom": "10px"}),
                    html.P("🟩 Green: Healthy/Dense Vegetation (NDVI > 0.6)", style={"textAlign": "center", "margin": "2px", "color": "#006400"}),
                    html.P("🟨 Yellow: Moderate Vegetation (NDVI ≈ 0.4–0.6)", style={"textAlign": "center", "margin": "2px", "color": "#DAA520"}),
                    html.P("⬜ White: Low or No Vegetation (NDVI < 0.2)", style={"textAlign": "center", "margin": "2px", "color": "#555555"}),
                ], style={"marginBottom": "20px"}),
                html.Div([
                    html.H4("California (2022)", style={"textAlign": "center", "color": "#000000"}),
                    html.Img(src="/static/2022_NVDI_CA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                    html.Pre("""// GEE NDVI for California (2022)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2022-01-01", "2022-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "California")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2022");""",
                        style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                    html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
                ], style={"marginBottom": "20px"}),
                html.Div([
                    html.H4("Georgia (2022)", style={"textAlign": "center", "color": "#000000"}),
                    html.Img(src="/static/2022_NVDI_GA_Map.png", style={"width": "100%", "borderRadius": "12px"}),
                    html.Pre("""// GEE NDVI for Georgia (2022)
var ndvi = ee.ImageCollection("MODIS/006/MOD13A2")
  .filterDate("2022-01-01", "2022-12-31")
  .select("NDVI")
  .mean()
  .clip(ee.FeatureCollection("TIGER/2018/States")
         .filter(ee.Filter.eq("NAME", "Georgia")));
Map.centerObject(ndvi, 6);
Map.addLayer(ndvi, {min: 0, max: 8000, palette: ['ffffff', 'ffff00', '00aa00']}, "NDVI 2022");""",
                        style={"backgroundColor": "#f4f4f4", "padding": "10px", "borderRadius": "8px", "fontSize": "13px", "overflowX": "auto", "color": "#000000"}),
                    html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
                ])
            ])
        else:  # Comparison view
            return html.Div([
                # Accessible, text-based NDVI color legend
                html.Div([
                    html.H4("NDVI Color Key", style={"textAlign": "center", "color": "#000000", "marginBottom": "10px"}),
                    html.P("🟩 Green: Healthy/Dense Vegetation (NDVI > 0.6)", style={"textAlign": "center", "margin": "2px", "color": "#006400"}),
                    html.P("🟨 Yellow: Moderate Vegetation (NDVI ≈ 0.4–0.6)", style={"textAlign": "center", "margin": "2px", "color": "#DAA520"}),
                    html.P("⬜ White: Low or No Vegetation (NDVI < 0.2)", style={"textAlign": "center", "margin": "2px", "color": "#555555"}),
                ], style={"marginBottom": "20px"}),
                html.Div([
                    html.H4("California: 2001 vs 2022", style={"textAlign": "center", "color": "#000000"}),
                    html.Div([
                        html.Div([
                            html.Img(
                                src="/static/2001_NVDI_CA_Map.png",
                                style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                            ),
                        ], style={"width": "49%", "marginRight": "2%"}),
                        html.Div([
                            html.Img(
                                src="/static/2022_NVDI_CA_Map.png",
                                style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                            ),
                        ], style={"width": "49%"})
                    ], style={"display": "flex", "justifyContent": "space-between", "marginBottom": "20px"}),
                    html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
                ]),
                html.Div([
                    html.H4("Georgia: 2001 vs 2022", style={"textAlign": "center", "color": "#000000"}),
                    html.Div([
                        html.Div([
                            html.Img(
                                src="/static/2001_NVDI_GA_Map.png",
                                style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                            ),
                        ], style={"width": "49%", "marginRight": "2%"}),
                        html.Div([
                            html.Img(
                                src="/static/2022_NVDI_GA_Map.png",
                                style={"width": "100%", "borderRadius": "12px", "height": "350px"}
                            ),
                        ], style={"width": "49%"})
                    ], style={"display": "flex", "justifyContent": "space-between"}),
                    html.A("View dataset (MODIS Vegetation NDVI)", href="https://lpdaac.usgs.gov/products/mod13a2v006/", target="_blank", style={"display": "block", "textAlign": "center", "marginBottom": "10px", "fontSize": "13px", "color": "#1a73e8"})
                ])
            ])

    # Callback to update year-slider value from drought-line-chart click
    @app.callback(
        Output('year-slider', 'value'),
        Input('drought-line-chart', 'clickData'),
        prevent_initial_call=True
    )
    def update_year_from_drought_chart(clickData):
        """
        Update the year slider when a point is clicked on the drought line chart.
        
        Args:
            clickData: Click data from the drought line chart
            
        Returns:
            int: Selected year from the clicked point
        """
        print("Drought chart clicked:", clickData)
        if clickData and 'points' in clickData and clickData['points']:
            selected_year = clickData['points'][0]['x']
            print("Selected year:", selected_year)
            if isinstance(selected_year, int):
                return selected_year
        raise exceptions.PreventUpdate