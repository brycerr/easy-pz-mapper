from src.classes.enums import BMColor


class Way:
    """Represents an OpenStreetMap way."""
    def __init__(self, way_id, nodes, tags=None):
        self.id = way_id
        self.nodes = nodes  # list of node types
        self.tags = tags or {}

    def __str__(self):
        return f"Way: {self.id}, Node Count: {len(self.nodes)}, Tags: {self.tags}"

    def get_way_style(self, way_type="highway"):
        return highway_styles.get(self.tags.get(way_type))


highway_styles = {
    # dictionary mapping highway types to colors.
    # format: (color, width)
    
    # Roads (main tags for the road network)
    "motorway":         (BMColor.DarkAsphalt, 8),
    "trunk":            (BMColor.DarkAsphalt, 8),
    "primary":          (BMColor.DarkAsphalt, 8),
    "secondary":        (BMColor.DarkAsphalt, 8),
    "tertiary":         (BMColor.DarkAsphalt, 8),
    "unclassified":     (BMColor.DarkAsphalt, 8),
    "residential":      (BMColor.DarkAsphalt, 8),

    # Link Roads
    "motorway_link":    (BMColor.DarkAsphalt, 8),
    "trunk_link":       (BMColor.DarkAsphalt, 8),
    "primary_link":     (BMColor.DarkAsphalt, 8),
    "secondary_link":   (BMColor.DarkAsphalt, 8),
    "tertiary_link":    (BMColor.DarkAsphalt, 8),

    # Special road types
    "living_street":    (BMColor.MediumAsphalt, 6),
    "service":          (BMColor.MediumAsphalt, 6),
    "pedestrian":       (BMColor.MediumAsphalt, 6),
    "track":            (BMColor.MediumAsphalt, 6),
    "bus_guideway":     (BMColor.MediumAsphalt, 6),
    "escape":           (BMColor.MediumAsphalt, 6),
    "raceway":          (BMColor.MediumAsphalt, 6),
    "road":             (BMColor.MediumAsphalt, 6),     # road of unknown type
    "busway":           (BMColor.MediumAsphalt, 6),

    # Paths
    "footway":          (BMColor.LightAsphalt, 1),
    "bridleway":        (BMColor.LightAsphalt, 1),
    "steps":            (BMColor.LightAsphalt, 1),
    "corridor":         (BMColor.LightAsphalt, 1),
    "path":             (BMColor.LightAsphalt, 1),
    "via_ferrata":      (BMColor.LightAsphalt, 1),

    # When sidewalk/crosswalk is tagged as a separate way (key=footway)
    "sidewalk":         (BMColor.LightAsphalt, 1),
    "crossing":         (BMColor.LightAsphalt, 1),
    "traffic_island":   (BMColor.LightAsphalt, 1),

    # When cycleway is drawn as its own way
    "cycleway":         (BMColor.LightAsphalt, 1)

    # add more here
}
