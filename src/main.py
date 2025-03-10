import os

from overpass import *
import overpass_api_query

from src.classes.Map import *
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
    input_map_name = "test_oop"
    map_name = sanitize_input(input_map_name)

    # dimensions of map in cells (cell is 300x300 tiles)
    #   the origin (0, 0) is based on the northwest most cell (top left)
    #   for reference, the B41 map is 65x52 cells
    # TODO: don't hardcode this here
    map_width_cells = 40  # west/east
    map_height_cells = 40  # north/south

    # real location info
    # TODO: don't hardcode this
    real_lat = 43.2
    real_lon = -88.716667
    real_radius = 12000

    # initialize map object
    pz_map = Map(map_name, map_width_cells, map_height_cells, real_lat, real_lon, real_radius)

    # initialize the map
    init_file_structure(map_name)

    pz_map.init_base_bmp()
    # TODO: base map grass noise, vegetation map
    # create_veg_map(map_name, width, height)

    # get data from the overpass api
    pz_map.set_ways(overpass_api_query.get_ways_from_point(real_lat, real_lon, real_radius))

    # draw ways
    pz_map.draw_ways()


def init_file_structure(map_name):
    """Sets up the proper file structure for the map."""
    # root map directory
    maps_dir = "../maps/" + map_name
    os.makedirs(maps_dir, exist_ok=True)

    # base bmp images
    bmp_dir = maps_dir + "/bmps"
    os.makedirs(bmp_dir, exist_ok=True)


def create_veg_map(map_name, width, height):
    # TODO: generation of the vegetation bmp image depends on a finalized base bmp image
    bmp_dir = "maps/" + map_name + "/bmps/"
    veg_path = map_name + "_veg.bmp"


def generate_roads(map_name):
    # TODO: road generation depends on either the google maps or openstreetmap api
    pass


if __name__ == '__main__':
    main()
