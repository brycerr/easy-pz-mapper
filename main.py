
import io
import os
import re

from enums import BMColor, VMColor

# TODO
#   [ ] Basic map generation functionality
#   [ ] ...
#   [ ] Upload real location using map
#   [ ] Convert map data to roads
#   [ ] Fill in houses
#   [ ] ...


def main():
    # name of the generated map
    # TODO: don't hardcode this here
    input_map_name = "test"
    # TODO: proper input validation
    map_name = re.sub(r"[^A-Za-z0-9]", "", input_map_name)   # removes non-alphanumeric characters from the string

    # dimensions of map in cells (cell is 300x300 tiles)
    #   the origin (0, 0) is based on the northwest (top left) most cell
    #   for reference, the B41 map is 65x52 cells
    # TODO: don't hardcode this here
    map_width_cells = 1  # west/east
    map_height_cells = 1  # north/south

    # generate the map
    init_file_structure(map_name)
    init_map(map_name, map_width_cells, map_height_cells)


def init_file_structure(map_name):
    """Sets up the proper file structure for the map."""
    # root map directory
    map_dir = "maps/" + map_name
    os.mkdir(map_dir)

    # base bmp images
    bmp_dir = map_dir + "/bmps"
    os.mkdir(bmp_dir)


def init_map(map_name, width, height):
    """Creates the base """
    create_base_map(map_name, width, height)
    create_veg_map(map_name, width, height)


def create_base_map(map_name, width, height):
    bmp_dir = "maps/" + map_name + "/bmps"
    base_path = map_name + "_base.bmp"


def create_veg_map(map_name, width, height):
    bmp_dir = "maps/" + map_name + "/bmps"


def generate_roads(map_name):
    # TODO
    pass


if __name__ == '__main__':
    main()
