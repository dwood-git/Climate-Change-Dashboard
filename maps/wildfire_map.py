""" 
This module generates a wildfire frequency map for California using raster data.
It utilizes rasterio for reading GeoTIFF files, matplotlib for creating image overlays,
and folium for generating interactive HTML maps with overlays.

Output:
- A transparent PNG overlay representing fire frequency
- An interactive HTML map with the overlay

Last updated: May 2025
"""

import rasterio
import numpy as np
import matplotlib.pyplot as plt
import folium

def generate_wildfire_map():
    # Load and read raster data
    with rasterio.open("data/california/California_FireFrequency_2001_2022.tif") as src:
        data = src.read(1)

    # Normalize and clean data
    normed_data = data.astype(float)
    # Replace non-positive values with NaN to ignore them in normalization
    normed_data[normed_data <= 0] = np.nan
    normed_data = normed_data / np.nanmax(normed_data)

    # Create and save PNG overlay
    plt.figure(figsize=(8, 10), dpi=300)
    # Use 'gist_heat' colormap to represent fire frequency intensity
    plt.imshow(normed_data, cmap='gist_heat', interpolation='nearest', vmin=0, vmax=1)
    plt.axis('off')
    plt.savefig("assets/maps/California_FireFrequency_Overlay.png", bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

    # Create and save Folium map
    wildfire_map = folium.Map(location=[36.5, -119], zoom_start=6)
    # Add image overlay with bounds matching California's geographic extent
    folium.raster_layers.ImageOverlay(
        image='assets/maps/California_FireFrequency_Overlay.png',
        bounds=[[32.0, -124.4], [42.1, -114.1]],
        opacity=0.6,  # Set overlay transparency
        name='Fire Frequency'
    ).add_to(wildfire_map)
    folium.LayerControl().add_to(wildfire_map)
    wildfire_map.save("assets/maps/california_fire_map.html")
