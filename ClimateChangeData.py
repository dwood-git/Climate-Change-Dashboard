import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import folium
import rasterio
import numpy as np
import matplotlib.colors as colors

# Load the GeoTIFF
with rasterio.open("assets/California_FireFrequency_2001_2022.tif") as src:
    data = src.read(1)

# Plot and save as PNG with colormap
# Normalize and clean data
normed_data = data.astype(float)
normed_data[normed_data <= 0] = np.nan  # Mask zero and negative values
normed_data = normed_data / np.nanmax(normed_data)

# Plot colormap
plt.figure(figsize=(8, 10), dpi=300)  # adds clarity
plt.imshow(normed_data, cmap='gist_heat', interpolation='nearest', vmin=0, vmax=1)
plt.axis('off')

# Save as a transparent overlay
plt.savefig("assets/California_FireFrequency_Overlay.png", bbox_inches='tight', pad_inches=0, transparent=True)
plt.close()

# --------------------------
# Generate the Folium wildfire map
# --------------------------
wildfire_map = folium.Map(location=[36.5, -119], zoom_start=6)

folium.raster_layers.ImageOverlay(
    image='assets/California_FireFrequency_Overlay.png',
    bounds=[[32.0, -124.4], [42.1, -114.1]],  # CA bounds
    opacity=0.6,
    name='Fire Frequency'
).add_to(wildfire_map)

folium.LayerControl().add_to(wildfire_map)

# Save as an embeddable HTML file
wildfire_map.save("assets/california_fire_map.html")


# -------------------------
# Initialize Flask App
# -------------------------
server = Flask(__name__)

# --------------------------
# Initialize Dash App with Flask Server
# --------------------------
app = Dash(__name__, server=server, url_base_pathname="/dashboard/")

# Application Layout
app.layout = html.Div([
    html.H1('Wildfire Climate Change Visualization Dashboard', style={'textAlign': 'center'}),
    html.H2("🔥 California Wildfire Frequency (2001–2022)", style={'textAlign': 'center'}),
    html.Iframe(
        srcDoc=open('assets/california_fire_map.html', 'r').read(),
        width='100%', height='600'
    )
])

# --------------------------
# Define Flask Route for Homepage
# --------------------------
@server.route("/")
def index():
    return "<h1>Welcome to the Climate Dashboard</h1><p>Visit <a href='/dashboard/'>Dashboard</a></p>"

# --------------------------
# Run the Integrated App
# --------------------------
if __name__ == "__main__":
    # Running the Flask server will serve both the Flask routes and the Dash app
    server.run(debug=True, port=5000)
  
