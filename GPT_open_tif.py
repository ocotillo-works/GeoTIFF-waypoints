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
import pyproj
from rasterio.warp import transform
import sys

# Path to your GeoTIFF file
geo_tiff_path = "./images/Fast-Ortho-Output-orthophoto.tif"

# List to store waypoints
waypoints = []


# Coordinate Reference System
# Function to reproject from the image's CRS to WGS84 (EPSG:4326)
def reproject_to_wgs84(x, y, src_crs, dst_crs='EPSG:4326'):
    """Reproject coordinates from one CRS to another (WGS84 by default)."""
    # Use pyproj to reproject coordinates
    transformer = pyproj.Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lat, lon


def onclick(event):
    """Handle mouse click events to add numbered waypoints and draw lines."""
    # Check if the toolbar is inactive (not in zoom or pan mode)
    if plt.get_current_fig_manager().toolbar.mode == '' and event.inaxes:
        # Get pixel coordinates from the click
        x_pixel, y_pixel = int(event.xdata), int(event.ydata)
        
        # Convert pixel coordinates to geographic coordinates (if needed)
        # x_coord,y_coord = rasterio.transform.xy(transform, y_pixel, x_pixel, offset='center')
        # waypoint_geo = Point(x_coord, y_coord)  # Shapely Point (for geographic reference)
        
        geo_coords = dataset.xy(y_pixel, x_pixel)  # This converts pixel to geographic coordinates
        # Reproject coordinates to WGS84 (if necessary)
        lat, lon = reproject_to_wgs84(geo_coords[0], geo_coords[1], dataset.crs)
        waypoint_geo = Point(lon, lat)  # Shapely Point (for geographic reference)
        

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


# Export waypoints to MAVLink .waypoints file
waypoints_filename = 'gen2.waypoints'
with open(waypoints_filename, 'w') as f:
    # Write header for the MAVLink file (QGroundControl WPL version)
    f.write("QGC WPL 110\n")  # Write header
    
    # Add home point (index 0)
    home_point = waypoints[0] if waypoints else None
    if home_point:
        # Home point command = 3, current WP = 1
        f.write(f"0\t1\t0\t3\t0\t0\t0\t0\t{home_point['geo'].y}\t{home_point['geo'].x}\t100.000000\t1\n")
    
    # Add waypoints starting from index 1 (regular waypoints)
    for index, waypoint in enumerate(waypoints[1:], start=1):
        # Waypoint command = 16
        f.write(f"{index}\t0\t0\t16\t0\t0\t0\t0\t{waypoint['geo'].y}\t{waypoint['geo'].x}\t100.000000\t1\n")

print(f"\nWaypoints have been exported to {waypoints_filename}")


