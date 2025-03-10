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

    def init_base_bmp(self):
        """Creates the base bitmap image."""
        self.base_path = f"../maps/{self.name}/bmps/{self.name}_base.bmp"

        bmp_width = self.width_cells * 300
        bmp_height = self.height_cells * 300

        # generate plain grass map
        tile_type = BMColor.DarkGrass.value
        Image.MAX_IMAGE_PIXELS = bmp_width * bmp_height
        img = Image.new("RGB", (bmp_width, bmp_height), tile_type)
        img.save(self.base_path)

    def draw_ways(self):
        bitmap = Image.open(self.base_path)
        draw = ImageDraw.Draw(bitmap)

        # calculate the bounds of the bitmap
        max_lat = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 0)[0]
        min_lat = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 180)[0]
        min_lon = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 270)[1]
        max_lon = find_point_from_distance_to_point(self.lat, self.lon, self.radius, 90)[1]
        bounds = min_lat, min_lon, max_lat, max_lon
        print("Types:")
        for x in bounds:
            print(type(x))

        # TODO: finish this properly based on way type
        #   idea -> different function that sorts & loops through ways, calling this one with the correct width & color
        # ====
        print("Plotting roads")
        dark_asphalt = BMColor.DarkAsphalt.value
        for way in self.ways:
            print(way)
            for i in range(len(way.nodes) - 1):
                node_1 = way.nodes[i]
                node_2 = way.nodes[i + 1]

                x1, y1 = map_to_bitmap(node_1.lat, node_1.lon, bitmap.width, bitmap.height, bounds)
                x2, y2 = map_to_bitmap(node_2.lat, node_2.lon, bitmap.width, bitmap.height, bounds)
                draw.line((x1, y1, x2, y2), fill=dark_asphalt, width=8, joint="curve")
        # ====

        bitmap.save(self.base_path)
        bitmap.show()

    # getters & setters

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


def find_point_from_distance_to_point(start_lat, start_lon, distance, angle):
    """Calculates a point based on distance from a starting point."""

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

    print(f"End: [{end_lat}, {end_lon}]")

    return [end_lat, end_lon]


def map_to_bitmap(lat, lon, width, height, bounds):
    min_lat, min_lon, max_lat, max_lon = bounds
    print(type(min_lon))
    x = int((lon - min_lon) / (max_lon - min_lon) * width)
    y = height - int((lat - min_lat) / (max_lat - min_lat) * height)
    return x, y


if __name__ == '__main__':
    test = find_point_from_distance_to_point(10, 10, 1000, 90)
    print(test)
