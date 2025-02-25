import overpy
from PIL import Image, ImageDraw

from enums import *
from utils import *


def generate_crappy_roads(base_path):
    # TODO: proof of concept, very messy code here. Location is currently hardcoded.
    #   This will need to be turned into functions eventually

    api = overpy.Overpass()

    # # UWW
    # hard_coded_distance = 600
    # hard_coded_location_coords = "42.839786, -88.743771"

    # Watertown
    hard_coded_distance = 12000
    hard_coded_location_coords = "43.2, -88.716667"

    # fetch all ways near Whitewater, WI
    result = api.query(f"""
        [out:json];
        (
            way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"];
        );
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

    # water
    result = api.query(f"""
        [out:json];
        (
            way(around:{hard_coded_distance},{hard_coded_location_coords})["natural"="water"];
            relation(around:{hard_coded_distance},{hard_coded_location_coords})["natural"="water"];
            way(around:{hard_coded_distance},{hard_coded_location_coords})["waterway"="riverbank"];
            relation(around:{hard_coded_distance},{hard_coded_location_coords})["waterway"="riverbank"];
        );
        out body;
        >;
        out skel qt;
    """)

    water = []
    for way in result.ways:
        water_coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
        distance = min(haversine_distance(location, coord) for coord in water_coords)
        water.append((distance, water_coords))

    water.sort()

    # service
    result = api.query(f"""
        [out:json];
        (
            way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="service"];
        );
        out body;
        >;
        out skel qt;
    """)

    services = []
    for way in result.ways:
        service_coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
        distance = min(haversine_distance(location, coord) for coord in service_coords)
        services.append((distance, service_coords))

    services.sort()

    # parking lots
    result = api.query(f"""
    [out:json];
    (
        way(around:{hard_coded_distance},{hard_coded_location_coords})["amenity"="parking"];
        relation(around:{hard_coded_distance},{hard_coded_location_coords})["amenity"="parking"];
        way(around:{hard_coded_distance},{hard_coded_location_coords})["parking"="surface"];
    );
    out body;
    >;
    out skel qt;
    """)

    parking_lots = []
    for way in result.ways:
        parking_lot_coords = [(float(node.lat), float(node.lon)) for node in way.nodes]
        distance = min(haversine_distance(location, coord) for coord in parking_lot_coords)
        parking_lots.append((distance, parking_lot_coords))

    parking_lots.sort()

    # footways
    result = api.query(f"""
        [out:json];
        (
            way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="footway"];
            way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="pedestrian"];
        );
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

    # roads
    result = api.query(f"""
    [out:json];
    (
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="motorway"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="trunk"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="primary"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="secondary"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="tertiary"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="unclassified"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="residential"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="motorway_link"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="trunk_link"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="primary_link"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="secondary_link"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="tertiary_link"];
      way(around:{hard_coded_distance},{hard_coded_location_coords})["highway"="living_street"];
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

    Image.MAX_IMAGE_PIXELS = 144000000
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

    print("Plotting medium grass")
    med_grass = BMColor.MediumGrass.value
    for _, (way_coords) in ways:
        for i in range(len(way_coords) - 1):
            coord1 = way_coords[i]
            coord2 = way_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=med_grass, width=40, joint="curve")

    print("Plotting light grass")
    light_grass = BMColor.LightGrass.value
    for _, (way_coords) in ways:
        for i in range(len(way_coords) - 1):
            coord1 = way_coords[i]
            coord2 = way_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=light_grass, width=25, joint="curve")

    # service
    print("Plotting medium asphalt")
    med_asphalt = BMColor.MediumAsphalt.value
    for _, service_coords in services:
        for i in range(len(service_coords) - 1):
            coord1 = service_coords[i]
            coord2 = service_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=med_asphalt, width=6, joint="curve")

    # parking lots
    print("Plotting parking lots")
    for _, parking_lot_coords in parking_lots:
        points = []
        for i in range(len(parking_lot_coords) - 1):
            coord1 = parking_lot_coords[i]
            coord2 = parking_lot_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            points.append(x1)
            points.append(y1)
            points.append(x2)
            points.append(y2)

        draw.polygon(points, fill=med_asphalt)

    # footways
    print("Plotting footways")
    light_asphalt = BMColor.LightAsphalt.value
    for _, footway_coords in footways:
        for i in range(len(footway_coords) - 1):
            coord1 = footway_coords[i]
            coord2 = footway_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=light_asphalt, width=1, joint="curve")

    # Plot the roads on the bitmap
    print("Plotting roads")
    road_tile = BMColor.DarkAsphalt.value
    for _, road_coords in roads:
        for i in range(len(road_coords) - 1):
            coord1 = road_coords[i]
            coord2 = road_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            draw.line((x1, y1, x2, y2), fill=road_tile, width=8, joint="curve")

    # water
    print("Plotting water")
    water_tile = BMColor.Water.value
    for _, water_coords in water:
        points = []
        for i in range(len(water_coords) - 1):
            coord1 = water_coords[i]
            coord2 = water_coords[i + 1]
            x1, y1 = map_to_bitmap(coord1[0], coord1[1], bitmap.width, bitmap.height, bounds)
            x2, y2 = map_to_bitmap(coord2[0], coord2[1], bitmap.width, bitmap.height, bounds)
            points.append(x1)
            points.append(y1)
            points.append(x2)
            points.append(y2)

        draw.polygon(points, fill=water_tile)

    bitmap.save('watertown.bmp')


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
