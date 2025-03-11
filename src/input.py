import utils


def get_map_data_input():
    input_map_name = input("Input your map's name: ")
    map_name = utils.sanitize_input(input_map_name)
    if map_name == "":  # default test value
        map_name = "test"

    # TODO: input validation/error handling
    input_map_width_cells = input("Input map width (west/east) in cells: ")
    if not input_map_width_cells:   # default test value
        input_map_width_cells = 40
    map_width_cells = int(input_map_width_cells)

    input_map_height_cells = input("Input map height (north/south) in cells: ")
    if not input_map_height_cells:  # default test value
        input_map_height_cells = 40
    map_height_cells = int(input_map_height_cells)

    # TODO: better coordinate selection: potentially drop a point on a map?
    # TODO: input validation/error handling
    input_lat = input("Input latitude: ")
    if not input_lat:   # default test value
        input_lat = 43.2
    lat = float(input_lat)

    input_lon = input("Input longitude: ")
    if not input_lon:   # default test value
        input_lon = -88.716667
    lon = float(input_lon)

    input_radius = input("Input radius (meters): ")
    if not input_radius:    # default test value
        input_radius = 12000
    radius = int(input_radius)

    map_data = [map_name, map_width_cells, map_height_cells, lat, lon, radius]

    return map_data
