
class Node:
    """Represents an OpenStreetMap node."""
    def __init__(self, node_id, lat, lon, tags=None):
        self.id = node_id
        self.lat = lat
        self.lon = lon
        self.tags = tags or {}

        # bitmap coordinates
        self.x = -1
        self.y = -1

    def __str__(self):
        return f"Node: {self.id} [{self.lat}, {self.lon}] Tags: {self.tags} | x,y: ({self.x}, {self.y})"

    def get_point(self):
        return self.x, self.y

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def set_tags(self, tags):
        for tag in tags:
            self.tags.append(tag)

    def get_tags(self):
        return self.tags

    def set_bitmap_coords(self, x, y):
        self.x = x
        self.y = y
