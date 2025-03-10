
class Way:
    """Represents an OpenStreetMap way."""
    def __init__(self, way_id, nodes, tags=None):
        self.id = way_id
        self.nodes = nodes  # list of node types
        self.tags = tags or {}

    def __str__(self):
        return f"Way: {self.id}, Node Count: {len(self.nodes)}, Tags: {self.tags}"
