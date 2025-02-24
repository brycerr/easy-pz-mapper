import overpy
from PIL import Image, ImageDraw

from enums import *
from utils import *


def generate_crappy_roads(base_path):
    # TODO: proof of concept, very messy code here

    api = overpy.Overpass()

    # fetch all ways near Whitewater, WI
    result = api.query("""
        [out:json];
        way(around:600,42.839786, -88.743771)["highway"];
        out body;
        >;
        out skel qt;
    """)

    location = (45.1400, -89.1500)
    ways = []
    for way in result.ways:
        way_coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
        distance = min(haversine_distance(location, coord) for coord in way_coords)
        ways.append((distance, way_coords))

    ways.sort()

    result = api.query("""
        [out:json];
        way(around:600,42.839786, -88.743771)["highway"="footway"];
        out body;
        >;
        out skel qt;
    """)

    footways = []
    for way in result.ways:
        footway_coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
        distance = min(haversine_distance(location, coord) for coord in footway_coords)
        footways.append((distance, footway_coords))

    footways.sort()

    result = api.query("""
    [out:json];
    (
      way(around:600,42.839786,-88.743771)["highway"="motorway"];
      way(around:600,42.839786,-88.743771)["highway"="trunk"];
      way(around:600,42.839786,-88.743771)["highway"="primary"];
      way(around:600,42.839786,-88.743771)["highway"="secondary"];
      way(around:600,42.839786,-88.743771)["highway"="tertiary"];
      way(around:600,42.839786,-88.743771)["highway"="unclassified"];
      way(around:600,42.839786,-88.743771)["highway"="residential"];
      way(around:600,42.839786,-88.743771)["highway"="motorway_link"];
      way(around:600,42.839786,-88.743771)["highway"="trunk_link"];
      way(around:600,42.839786,-88.743771)["highway"="primary_link"];
      way(around:600,42.839786,-88.743771)["highway"="secondary_link"];
      way(around:600,42.839786,-88.743771)["highway"="tertiary_link"];
      way(around:600,42.839786,-88.743771)["highway"="living_street"];
      way(around:600,42.839786,-88.743771)["highway"="service"];
    );
    out body;
    >;
    out skel qt;
    """)

    roads = []
    for way in result.ways:
        road_coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
        distance = min(haversine_distance(location, coord) for coord in road_coords)
        roads.append((distance, road_coords))

    roads.sort()

    bitmap = Image.open(base_path)
    draw = ImageDraw.Draw(bitmap)

    # Calculate the bounds for the bitmap
    all_coords = [coord for _, road_coords in ways for coord in road_coords]
    min_lat = min(coord[0] for coord in all_coords)
    max_lat = max(coord[0] for coord in all_coords)
    min_lon = min(coord[1] for coord in all_coords)
    max_lon = max(coord[1] for coord in all_coords)
    bounds = (min_lat, min_lon, max_lat, max_lon)

    # # Plot the nodes on the bitmap
    # road_tile = BMColor.DarkAsphalt.value
    # for _, road_coords in roads:
    #     for coord in road_coords:
    #         x, y = map_to_bitmap(coord[0], coord[1], bitmap.width, bitmap.height, bounds)
    #         draw.point((x, y), fill=road_tile)

    med_grass = BMColor.MediumGrass.value
    for _, (way_coords) in ways:
        for i in range(len(way_coords) - 1):
            coord1 = way_coords[i]
            coord2 = way_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=med_grass, width=40, joint="curve")

    light_grass = BMColor.LightGrass.value
    for _, (way_coords) in ways:
        for i in range(len(way_coords) - 1):
            coord1 = way_coords[i]
            coord2 = way_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=light_grass, width=25, joint="curve")

    # footways
    light_asphalt = BMColor.LightAsphalt.value
    for _, footway_coords in footways:
        for i in range(len(footway_coords) - 1):
            coord1 = footway_coords[i]
            coord2 = footway_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=light_asphalt, width=2, joint="curve")

    # Plot the roads on the bitmap
    road_tile = BMColor.DarkAsphalt.value
    for _, road_coords in roads:
        for i in range(len(road_coords) - 1):
            coord1 = road_coords[i]
            coord2 = road_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=road_tile, width=10, joint="curve")

    bitmap.save('less_crappy_map.png')


# Function to map coordinates to bitmap pixels
def map_to_bitmap(lat, lon, width, height, bounds):
    min_lat, min_lon, max_lat, max_lon = bounds
    x = int((lon - min_lon) / (max_lon - min_lon) * width)
    y = height - int((lat - min_lat) / (max_lat - min_lat) * height)
    return x, y


def test():
    api = overpy.Overpass()

    # fetch all ways and nodes
    result = api.query("""
    way(50.746,7.154,50.748,7.157) ["highway"];
    (._;>;);
    out body;
    """)

    for way in result.ways:
        print("Name: %s" % way.tags.get("name", "n/a"))
        print("  Highway: %s" % way.tags.get("highway", "n/a"))
        print("  Nodes:")
        for node in way.nodes:
            print("    Lat: %f, Lon: %f" % (node.lat, node.lon))


if __name__ == '__main__':
    test()
