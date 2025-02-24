
import io
import os

from PIL import Image

from enums import *
from overpass import *
from utils import *

# TODO
#   [x] Basic map generation functionality
#   [ ] Refactor this into a map object
#   [ ] ...
#   [ ] Upload arbitrary real location using map
#   [ ] Convert map data to good roads
#   [ ] Fill in houses
#   [ ] ...


def main():
    # name of the generated map
    # TODO: don't hardcode this here
    input_map_name = "test"
    map_name = sanitize_input(input_map_name)

    # dimensions of map in cells (cell is 300x300 tiles)
    #   the origin (0, 0) is based on the northwest most cell (top left)
    #   for reference, the B41 map is 65x52 cells
    # TODO: don't hardcode this here
    map_width_cells = 4  # west/east
    map_height_cells = 4  # north/south

    # generate the map
    init_file_structure(map_name)
    init_map(map_name, map_width_cells, map_height_cells)


def init_file_structure(map_name):
    """Sets up the proper file structure for the map."""
    # root map directory
    maps_dir = "maps/" + map_name
    os.makedirs(maps_dir, exist_ok=True)

    # base bmp images
    bmp_dir = maps_dir + "/bmps"
    os.makedirs(bmp_dir, exist_ok=True)


def init_map(map_name, map_width_cells, map_height_cells):
    """Creates the base bitmap images"""
    width = map_width_cells * 300
    height = map_height_cells * 300

    base_path = init_base_map(map_name, width, height)
    # TODO: base map noise, roads, vegetation
    # create_veg_map(map_name, width, height)

    generate_crappy_roads(base_path)


def init_base_map(map_name, width, height):
    bmp_dir = "maps/" + map_name + "/bmps/"
    base_path = bmp_dir + map_name + "_base.bmp"

    # generate plain grass map
    tile_type = BMColor.DarkGrass.value
    img = Image.new("RGB", (width, height), tile_type)
    img.save(base_path)

    return base_path


def create_veg_map(map_name, width, height):
    # TODO: generation of the vegetation bmp image depends on a finalized base bmp image
    bmp_dir = "maps/" + map_name + "/bmps/"
    veg_path = map_name + "_veg.bmp"


def generate_roads(map_name):
    # TODO: road generation depends on either the google maps or openstreetmap api
    pass


if __name__ == '__main__':
    main()
