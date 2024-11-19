# GeoTIFF-waypoints
Open a GeoTIFF image, click to add mission waypoints, then export your plan.


## TODO
- [x] Zoom/enhance visual size of tif
- [x] Number the waypoints
- [x] Draw lines between waypoints
- [x] Export plan to a file to use in Mission Planner

### Usability & Quality of Life
- [ ] Input GeoTIFFs exceed GitHub 100MB input file size limit. Might need LFS.
- [ ] Script to set up requirements, environment.


# Geo-Referenced Waypoints with Python

This project allows users to click on a GeoTIFF image, add waypoints at the clicked locations, and view the corresponding geographic coordinates. The project also allows users to draw lines between sequential waypoints and export these waypoints in a format suitable for mission planning software.

## Features
- Click on a GeoTIFF image to add waypoints with geographic coordinates (latitude, longitude).
- Display waypoints with sequential numbering and the ability to draw arrows between them.
- Export waypoints in a format compatible with mission planning software like Mission Planner.

## Installation

To set up the project on your local machine, follow these steps:

### 1. Clone the Repository

If you haven't already, clone the repository:

```bash
git clone <your_project_repo_url>
cd <your_project_directory>
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

Create a virtual environment to manage dependencies:

- Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
- macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 3. Install Dependencies

Install all required dependencies using `pip`:

`pip install -r requirements.txt`

This will install all the necessary libraries for running the project.

### 4. Set Up Logging (Optional)

If you want to log detailed output during execution, ensure that logging is properly configured. The project uses Python’s built-in `logging` library to log debug and info messages.

## Usage

### 1. Run the Script

To run the script, simply execute the Python file:

`python <your_script_name>.py`

The script will open the GeoTIFF image, and you can click on the image to add waypoints. Each click will:

- Add a new waypoint to the list with geographic coordinates.
- Display a red dot on the image marking the waypoint.
- Draw lines between sequential waypoints with arrows indicating the order.

### 2. Interacting with the Image

- **Click on the image** to add waypoints.
- The waypoints will be displayed on the image with their respective numbers.
- Arrows will be drawn between sequential waypoints.
- Waypoints' geographic coordinates are printed in the console and logged for reference.

### 3. Export Waypoints

Waypoints can be exported to a file format compatible with mission planning software, such as Mission Planner or MAVLink.

### Example of Exported Waypoint Format:

```
0 1 3 16 0 0 0 0 41.0358872 -83.3071187 256.010000 1 1 0 3 16 0.00000000 0.00000000 0.00000000 0.00000000 41.03609760 -83.30700870 100.000000 1
```

### 4. Logging Output (Debugging)

To enable detailed logging, you can configure the logging level to `DEBUG` in the script. This will print additional information to the console, such as:

- Mouse click coordinates
- Geographic coordinates (latitude, longitude)
- Waypoint details

This helps to troubleshoot and ensure everything is working as expected.

## Development

To contribute to this project, feel free to fork the repository, make your changes, and create a pull request. Please make sure to test your changes before submitting.

### Updating Dependencies

If you add new dependencies to the project, be sure to update the `requirements.txt` file by running:

`pip freeze > requirements.txt`

This will update the file with the latest versions of the installed packages.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
