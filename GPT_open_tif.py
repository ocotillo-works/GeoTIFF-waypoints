# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 08:55:03 2024

@author: kjcer
"""

import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from shapely.geometry import Point

# Path to your GeoTIFF file
geo_tiff_path = "./images/Fast-Ortho-Output-orthophoto.tif"

# List to store waypoints
waypoints = []

def onclick(event):
    """Handle mouse click events to add waypoints."""
    # Get pixel coordinates
    x_pixel, y_pixel = event.xdata, event.ydata
    if x_pixel is not None and y_pixel is not None:
        # Convert pixel to geospatial coordinates
        x_geo, y_geo = rasterio.transform.xy(transform, int(y_pixel), int(x_pixel), offset="center")
        waypoints.append(Point(x_geo, y_geo))
        print(f"Added waypoint: ({x_geo}, {y_geo})")
        
        # Plot waypoint
        plt.plot(x_pixel, y_pixel, 'ro')
        plt.draw()

# Open the GeoTIFF file
with rasterio.open(geo_tiff_path) as dataset:
    # Get transformation data for georeferencing
    transform = dataset.transform

    # Plot the GeoTIFF
    fig, ax = plt.subplots()
    show(dataset, ax=ax)
    plt.title("Click to add waypoints")

    # Connect the onclick event to the plot
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

# Print all waypoints after the interaction
print("Waypoints (georeferenced):")
for waypoint in waypoints:
    print(waypoint)
