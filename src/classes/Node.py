
class Node:
    """Represents an OpenStreetMap node."""
    def __init__(self, node_id, lat, lon, tags=None):
        self.id = node_id
        self.lat = lat
        self.lon = lon
        self.tags = tags or {}

    def __str__(self):
        return f"Node: {self.id} [{self.lat}, {self.lon}] Tags: {self.tags}"

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def set_tags(self, tags):
        for tag in tags:
            self.tags.append(tag)

    def get_tags(self):
        return self.tags
