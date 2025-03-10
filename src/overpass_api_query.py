import overpy

from src.classes.Node import *
from src.classes.Way import *


def get_ways_from_point(lat, lon, radius):
    """Query the overpass API for all ways around a given point (lat, lon) and radius (meters)."""

    api = overpy.Overpass()

    query = f"""
        [out:json];
        (
            way(around:{radius},{lat},{lon});
        );
        out body;
        >;
        out skel qt;
    """

    result = api.query(query)

    # process the ways
    ways = []
    for way in result.ways:
        # current way's nodes
        temp_nodes = []
        for node in way.nodes:
            temp_node = Node(node.id, node.lat, node.lon)
            temp_nodes.append(temp_node)

        temp_way = Way(way.id, temp_nodes, way.tags)

        ways.append(temp_way)
    return ways


# FOR TESTING PURPOSES
if __name__ == '__main__':
    print("RUNNING TEST: overpass_api_query\n")

    muldraugh_lat = 37.936944
    muldraugh_lon = -85.991389
    muldraugh_radius = 1000
    muldraugh_ways = get_ways_from_point(muldraugh_lat, muldraugh_lon, muldraugh_radius)

    for way in muldraugh_ways:
        print(way)
