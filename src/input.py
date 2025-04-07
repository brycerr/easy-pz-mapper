import utils


def get_map_data_input():
    input_map_name = input("Input your map's name: ")
    map_name = utils.sanitize_input(input_map_name)
    if map_name == "":  # default test value
        map_name = "test"

    # TODO: better coordinate selection: potentially drop a point on a map?
    # TODO: input validation/error handling
    input_lat = input("Input latitude: ")
    if not input_lat:   # default test value
        input_lat = 42.83
    lat = float(input_lat)

    input_lon = input("Input longitude: ")
    if not input_lon:   # default test value
        input_lon = -88.74
    lon = float(input_lon)

    input_radius = input("Input radius (meters): ")
    if not input_radius:    # default test value
        input_radius = 3000
    radius = int(input_radius)

    # TODO: input validation/error handling
    cell_size = 300     # TODO: move this to a global enum

    input_map_width_cells = input("Input map width (west/east) in cells: ")
    if not input_map_width_cells:   # default test value
        input_map_width_cells = round(radius / cell_size)
    map_width_cells = int(input_map_width_cells)

    input_map_height_cells = input("Input map height (north/south) in cells: ")
    if not input_map_height_cells:  # default test value
        input_map_height_cells = round(radius / cell_size)
    map_height_cells = int(input_map_height_cells)

    print()

    map_data = [map_name, map_width_cells, map_height_cells, lat, lon, radius]

    return map_data


def select_mode():
    """Allows user to select to load stored data or to query Overpass for new data."""
    selection_prompt = "Select Mode:\n" \
                       " [0] Exit\n" \
                       " [1] Load Stored Map Data\n" \
                       " [2] Generate New Map Data\n"
    print(selection_prompt)

    mode = int(input("Input option number: "))
    while 0 > mode or mode > 2:
        print("Invalid input. Please type the number of the mode you would like to select.")
        print(selection_prompt)

        mode = int(input("Input option number: "))

    if mode == 0:
        print("Exiting program.")
        exit()
    elif mode == 1:
        # TODO: load data
        print("Selected: ")
        pass
    elif mode == 2:
        print("Selected: Generate New Map Data\n")
        return get_map_data_input()


if __name__ == "__main__":
    select_mode()
