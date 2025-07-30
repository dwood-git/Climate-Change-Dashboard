"""
Main Flask-Dash application entry point.

This module initializes the Flask server and Dash application,
sets up data loading, and configures the main application structure.
"""

from flask import Flask
from dash import Dash
from components.layout import get_main_layout
from components.callbacks import register_callbacks
from routes.home import home_bp
from data.data_manager import DataManager
import os

def create_app():
    """
    Factory function to create and configure the Flask-Dash application.
    
    Returns:
        Flask: Configured Flask application instance
    """
    # Initialize Flask server
    server = Flask(__name__)
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Initialize Dash app
    app = Dash(
        __name__, 
        server=server, 
        url_base_pathname="/dashboard/",
        suppress_callback_exceptions=True
    )
    
    # Set the layout
    app.layout = get_main_layout()
    
    # Register callbacks
    register_callbacks(app, data_manager)
    
    # Register Flask blueprints
    server.register_blueprint(home_bp)
    
    # Add default route
    @server.route("/")
    def index():
        return server.redirect("/home")
    
    return server

# Create the server instance for Heroku deployment
server = create_app()

if __name__ == "__main__":
    server.run(debug=True, port=8050)