import datetime
import decimal
import math

from PIL import Image, ImageDraw

from src.classes.enums import BMColor


class Map:
    def __init__(self, name, width_cells, height_cells, lat, lon, radius, ways=None):
        self.name = name
        self.width_cells = width_cells
        self.height_cells = height_cells
        self.lat = lat
        self.lon = lon
        self.radius = radius    # radius from lat/lon (meters)
        self.ways = ways or []
        self.base_path = ""     # base bitmap filepath
        self.veg_path = ""      # veg bitmap filepath

        # technical constants (potentially move this elsewhere to make it more accessible?)
        self.CELL_SIZE = 300    # changed to 256 in B42 (supposedly doesn't affect map making?)
        self.CHUNK_SIZE = 10    # changed to 8 in B42 (supposedly doesn't affect map making?)

    def init_base_bmp(self):
        """Creates the base bitmap image."""
        self.base_path = f"../maps/{self.name}/bmps/{self.name}_base.bmp"

        bmp_width = self.width_cells * self.CELL_SIZE
        bmp_height = self.height_cells * self.CELL_SIZE

        # generate plain grass map
        tile_type = BMColor.DarkGrass.value
        Image.MAX_IMAGE_PIXELS = bmp_width * bmp_height
        img = Image.new("RGB", (bmp_width, bmp_height), tile_type)
        img.save(self.base_path)

    def draw_ways(self):
        bitmap = Image.open(self.base_path)
        # draw = ImageDraw.Draw(bitmap)

        # calculate the bounds of the bitmap
        max_lat = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 0)[0]
        min_lat = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 180)[0]
        min_lon = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 270)[1]
        max_lon = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 90)[1]
        bounds = min_lat, min_lon, max_lat, max_lon

        layers = {}     # dictionary to store drawing layers based on color
        unknowns = set()   # for reporting unknown way types to unknown.txt

        print("Drawing ways...")
        for way in self.ways:
            # print(way)

            way_style = way.get_way_style()
            if way_style is None:   # skip this way
                # report it to unknown.txt file for debug purposes
                unknowns.add(way.tags.get("highway"))
                continue

            way_color = way_style[0].value
            way_width = way_style[1]

            # create a new layer for the way color if it doesn't exist
            if way_color not in layers:
                layer_image = Image.new("RGBA", (bitmap.width, bitmap.height), (0, 0, 0, 0))
                layer_draw = ImageDraw.Draw(layer_image)
                layers[way_color] = (layer_image, layer_draw)

            # draw line on the corresponding layer
            layer_draw = layers[way_color][1]
            for i in range(len(way.nodes) - 1):
                node_1 = way.nodes[i]
                node_2 = way.nodes[i + 1]

                x1, y1 = map_to_bitmap(node_1.lat, node_1.lon, bitmap.width, bitmap.height, bounds)
                x2, y2 = map_to_bitmap(node_2.lat, node_2.lon, bitmap.width, bitmap.height, bounds)
                layer_draw.line((x1, y1, x2, y2), fill=way_color, width=way_width, joint="curve")

                # record bitmap coordinates (easier for hill climbing optimizer to work with)
                node_1.set_bitmap_coords(x1, y1)
                node_2.set_bitmap_coords(x2, y2)

        # merge all layers onto the base bitmap
        sorted_layers = sorted(layers.keys(), key=get_color_layer_sort_order)

        for color in sorted_layers:
            layer_image = layers[color][0]
            bitmap = Image.alpha_composite(bitmap.convert("RGBA"), layer_image)

        # report unknown way types
        if len(unknowns) > 0:
            file = open("../testing/unknown.txt", "a")
            file.write(f"\n[{datetime.datetime.utcnow()}] UNKNOWN WAY TYPES")
            for way_type in unknowns:
                if way_type is not None:
                    file.write(f"\n> {way_type}")

        # save the bitmap
        bitmap.save(self.base_path)
        bitmap.show(title=f"{self.name} Base Bitmap")

    def draw_using_xy(self, padding=20, way_color=(0, 0, 0)):
        # TODO: CLEAN THIS UP
        # Gather all unique nodes from ways
        unique_nodes = set()
        for way in self.ways:
            unique_nodes.update(way.nodes)

        # Create image
        bmp_width = self.width_cells * self.CELL_SIZE
        bmp_height = self.height_cells * self.CELL_SIZE
        img = Image.new("RGB", (bmp_width, bmp_height), color="white")
        draw = ImageDraw.Draw(img)

        # Draw ways
        for way in self.ways:
            if len(way.nodes) < 2:
                continue
            points = [(node.x, node.y) for node in way.nodes]
            draw.line(points, fill=way_color, width=2)

        # save the bitmap
        img.save(f"../maps/{self.name}/bmps/{self.name}_base_opt.bmp")
        img.show(title=f"{self.name} Base Bitmap")

    def save_map(self):
        # TODO: save map data (including ways & nodes) to a file
        return

    def load_map(self):
        # TODO: load map data from file
        return

    # getters & setters

    def get_way_count(self):
        way_count = 0
        for way in self.ways:
            is_relevant = False
            for tag in way.tags:
                if tag == "highway":
                    is_relevant = True
            if not is_relevant:
                break
            way_count += len(way.nodes)
        return way_count

    def get_ways(self):
        return self.ways

    def set_ways(self, ways):
        self.ways = ways

    # TODO: remove?
    def append_ways(self, new_ways):
        self.ways.append(new_ways)

    def set_base_path(self, filepath):
        self.base_path = filepath

    def set_veg_path(self, filepath):
        self.veg_path = filepath


def get_color_layer_sort_order(color):
    """Returns the sort order of a given color based on the BMColor enum."""
    try:
        return list(BMColor).index(BMColor(color))
    except ValueError:
        return len(BMColor)     # return a high value for unknown colors


def find_point_from_distance_to_point(start_lat, start_lon, distance, angle):
    """
    Calculates a point based on distance from a starting point.

    Reference: https://www.movable-type.co.uk/scripts/latlong.html
    """

    # print(f"Start: [{start_lat}, {start_lon}], Distance: {distance}, Angle: {angle}")

    # convert degrees to radians
    lat_1 = math.radians(start_lat)
    lon_1 = math.radians(start_lon)
    bearing = math.radians(angle)

    r = 6371 * 1000     # radius of Earth (meters)
    angular_dist = distance / r

    lat_2 = math.asin(math.sin(lat_1) * math.cos(angular_dist) +
                      math.cos(lat_1) * math.sin(angular_dist) * math.cos(bearing))

    lon_2 = lon_1 + math.atan2(math.sin(bearing) * math.sin(angular_dist) * math.cos(lat_1),
                               math.cos(angular_dist) - math.sin(lat_1) * math.sin(lat_2))

    # convert radians to degrees
    end_lat = decimal.Decimal(math.degrees(lat_2))
    end_lon = decimal.Decimal(math.degrees(lon_2))

    # print(f"End: [{end_lat}, {end_lon}]")

    return [end_lat, end_lon]


def map_to_bitmap(lat, lon, width, height, bounds):
    min_lat, min_lon, max_lat, max_lon = bounds
    x = int((lon - min_lon) / (max_lon - min_lon) * width)
    y = height - int((lat - min_lat) / (max_lat - min_lat) * height)
    return x, y


if __name__ == '__main__':
    test = find_point_from_distance_to_point(10, 10, 1000, 90)
    print(test)
