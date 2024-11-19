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
waypoints_pixel = []

def onclick(event):
    """Handle mouse click events to add numbered waypoints and draw lines."""
    # Check if the toolbar is inactive (not in zoom or pan mode)
    if plt.get_current_fig_manager().toolbar.mode == '' and event.inaxes:
        # Get pixel coordinates from the click
        x_pixel, y_pixel = int(event.xdata), int(event.ydata)
        
        # Convert pixel coordinates to geographic coordinates (if needed)
        x_coord,y_coord = rasterio.transform.xy(transform, y_pixel, x_pixel, offset='center')
        waypoint_geo = Point(x_coord, y_coord)  # Shapely Point (for geographic reference)
        
        # Generate the waypoint number
        waypoint_number = len(waypoints) + 1

        # Store both the pixel coordinates and geographic coordinates
        waypoint = {
            'number': waypoint_number,
            'pixel': (x_pixel, y_pixel),
            'geo': waypoint_geo
        }
        waypoints.append(waypoint)
        

        ax.plot(event.xdata, event.ydata, 'ro', markersize=6) # Plot the waypoint on the map        
        # Annotate the point with its number
        ax.text(event.xdata, event.ydata, str(waypoint_number), color='yellow', fontsize=10, ha='left', va='bottom')
        
        # If there are at least two points, draw a line between the last two waypoints (using pixel coordinates)
        if len(waypoints) > 1:
            prev_x, prev_y = waypoints[-2]['pixel']
            curr_x, curr_y = waypoints[-1]['pixel']
            
            # Draw a line between the last two waypoints using pixel coordinates
            # ax.plot([prev_x, curr_x], [prev_y, curr_y], 'g-', linewidth=1)  # Green line
            
            # Draw an arrow between the last two waypoints using pixel coordinates
            ax.annotate('', xy=(curr_x, curr_y), xytext=(prev_x, prev_y),
                        arrowprops=dict(facecolor='green', edgecolor='green', arrowstyle='->', lw=1))  # Green arrow


        # Redraw the figure to show the point and the line
        fig.canvas.draw()
        
        # Print feedback to the console (show both pixel and geographic coordinates)
        print(f"Added waypoint {len(waypoints)}:")
        print(f"  Pixel Coordinates: {waypoints[-1]['pixel']}")
        print(f"  Geographic Coordinates: {waypoints[-1]['geo']}")
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
