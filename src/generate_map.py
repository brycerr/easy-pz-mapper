import os

from classes.Map import *
import overpass_api_query


def generate(map_data):
    pz_map = init_map(map_data)
    draw_ways(pz_map)

    return pz_map


def init_map(map_data):
    # process user input
    map_name, map_width_cells, map_height_cells, lat, lon, radius = map_data

    # initialize the map
    init_file_structure(map_name)

    # initialize map object
    pz_map = Map(map_name, map_width_cells, map_height_cells, lat, lon, radius)

    pz_map.init_base_bmp()
    # TODO: base map grass noise, vegetation map
    # create_veg_map(map_name, width, height)

    # get data from the overpass api
    # TODO: this assumes the map is square, fix this for non-square maps
    adjusted_radius = math.sqrt(2 * (radius ** 2))  # ensures all appropriate ways are fetched
    # print(f"Adjusted Radius: {adjusted_radius}")

    # TODO: edit this during store/load data update
    ways = overpass_api_query.get_ways_from_point(lat, lon, adjusted_radius)
    pz_map.set_ways(ways)

    return pz_map


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


def draw_ways(pz_map):
    # draw roads
    pz_map.draw_ways()
