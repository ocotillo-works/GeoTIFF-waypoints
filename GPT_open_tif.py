# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 08:55:03 2024

@author: kjcer
"""

import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
from shapely.geometry import Point
import sys

# Path to your GeoTIFF file
geo_tiff_path = "./images/Fast-Ortho-Output-orthophoto.tif"

# List to store waypoints
waypoints = []

def onclick(event):
    """Handle mouse click events to add waypoints."""
    # Check if the toolbar is inactive (not in zoom or pan mode)
    if plt.get_current_fig_manager().toolbar.mode == '' and event.inaxes:  # Ensure the click is within the plot
        # Get pixel coordinates from the click
        x_pixel, y_pixel = int(event.xdata), int(event.ydata)
        
        # Convert pixel coordinates to geographic coordinates
        x_coord,y_coord = rasterio.transform.xy(transform, y_pixel, x_pixel, offset='center')
        
        # Add the waypoint as a Shapely Point
        waypoint = Point(x_coord, y_coord)
        waypoints.append(waypoint)
        
        # Plot the waypoint on the map
        ax.plot(event.xdata, event.ydata, 'ro', markersize=6, label="Waypoint" if len(waypoints) == 1 else "")
        
        # Annotate the point with its number
        ax.text(event.xdata, event.ydata, str(len(waypoints)), color='yellow', fontsize=12, ha='left', va='bottom')

        fig.canvas.draw()  # Redraw the figure to show the point
        
        # Print feedback to the console
        print(f"Added waypoint: {waypoint}")
        plt.pause(0.1)  # Ensure console output updates in real time
        sys.stdout.flush()  # Force the console to update immediately

        
# Open the GeoTIFF file
with rasterio.open(geo_tiff_path) as dataset:
    # Get transformation data for georeferencing
    transform = dataset.transform

    # Plot the GeoTIFF
    fig, ax = plt.subplots(figsize=(10, 10))
    show(dataset, ax=ax, title="Click to Add Waypoints")

    # Add a crosshair cursor for precision
    cursor = Cursor(ax, useblit=True, color='green', linewidth=1)

     # Maximize the plot window but keep it windowed
    mng = plt.get_current_fig_manager()
    try:
        mng.window.state('zoomed')  # Works for TkAgg backend (maximize)
    except AttributeError:
        mng.resize(*mng.window.maxsize())  # For other backends, resize to screen size


    # Connect the onclick event to the plot
    fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()




# Print all waypoints after the interaction
print("Waypoints (georeferenced):")
for waypoint in waypoints:
    print(waypoint)
