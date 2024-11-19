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
import logging



# How much LOG??
LOG_LEVEL=logging.INFO

# Path to your GeoTIFF file
geo_tiff_path = "./images/ESPG-4326-orthophoto.tif"

# List to store waypoints
waypoints = []


# Prepare file logging
def setup_logger(name="waypoint_logger", log_level=logging.DEBUG):
    """
    Set up a logger for the script with a given name and log level.
    
    Args:
    - name (str): Name of the logger.
    - log_level (int): Logging level (e.g., logging.DEBUG, logging.INFO).
    
    Returns:
    - logger (logging.Logger): Configured logger instance.
    """
    # Create a custom logger
    logger = logging.getLogger("waypoint_logger")
    logger.setLevel(logging.DEBUG)  # Set the base level for your logger

    # Create a console handler for output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the handler's log level

    # Create a formatter and associate it with the handler
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)

    # Add the handler to the custom logger
    logger.addHandler(console_handler)
    return logger


# Coordinate Reference System
# Function to reproject from the image's CRS to WGS84 (EPSG:4326)
def reproject_to_wgs84(x, y, src_crs, dst_crs='EPSG:4326'):
    """Reproject coordinates from one CRS to another (WGS84 by default)."""
    logger.debug(f"src_crs: {src_crs}, dst_crs: {dst_crs}")
    if (src_crs == dst_crs):
        logger.debug(f"Same CRS: {src_crs}")
        return x,y

    # Use pyproj to reproject coordinates
    transformer = pyproj.Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lat, lon


def onclick(event):
    """Handle mouse click events to add numbered waypoints and draw lines."""
    # Check if the toolbar is inactive (not in zoom or pan mode)
    if plt.get_current_fig_manager().toolbar.mode == '' and event.inaxes:
        x_pixel, y_pixel = event.xdata, event.ydata # Get pixel coordinates from the click
        
        # geo_coords = dataset.xy(y_pixel, x_pixel)  # This converts pixel to geographic coordinates
        lon, lat = reproject_to_wgs84(x_pixel, y_pixel, dataset.crs)

        logger.debug(f"Clicked pixel coordinates: x={x_pixel}, y={y_pixel}")
        logger.debug(f"Interpreted geographic coordinates (WGS84): lat={lat}, lon={lon}")

        # Create and store waypoint
        waypoint_geo = Point(lon, lat)  # Shapely Point (for geographic reference)
        waypoint_number = len(waypoints) + 1
        waypoint = {
            'number': waypoint_number,
            'pixel': (event.xdata, event.ydata),
            'geo': waypoint_geo
        }
        waypoints.append(waypoint)
        
        # Plot and annotate the waypoint
        ax.plot(event.xdata, event.ydata, 'ro', markersize=6)     
        ax.text(event.xdata, event.ydata, str(waypoint_number), color='yellow', fontsize=10, ha='left', va='bottom')
        
        # Draw lines with arrows between waypoints
        if len(waypoints) > 1:
            prev_x, prev_y = waypoints[-2]['pixel']
            curr_x, curr_y = waypoints[-1]['pixel']
            ax.annotate('', xy=(curr_x, curr_y), xytext=(prev_x, prev_y),
                        arrowprops=dict(facecolor='green', edgecolor='green', arrowstyle='->', lw=1))  # Green arrow

        # Redraw the figure to show the point and the line
        fig.canvas.draw()
        
        # Log waypoint info
        logger.info(f"Added waypoint {waypoint_number}:")
        logger.info(f"  Pixel Coordinates: {waypoints[-1]['pixel']}")
        logger.info(f"  Geographic Coordinates: {waypoints[-1]['geo']}")
        # sys.stdout.flush()  # Force the console to update immediately


# ========================================
# Main Business
# ========================================
logger = setup_logger(name="waypoint_logger", log_level=LOG_LEVEL)

# Open the GeoTIFF file
with rasterio.open(geo_tiff_path) as dataset:
    # Get transformation data for georeferencing
    transform = dataset.transform

    # Plot the GeoTIFF
    fig, ax = plt.subplots(figsize=(12, 12))
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
logger.debug("Waypoints (georeferenced):")
for waypoint in waypoints:
    logger.debug(waypoint)


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

logger.info(f"\nWaypoints have been exported to {waypoints_filename}")


