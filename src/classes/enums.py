from enum import Enum


# BITMAP COLORS

class BMColor(Enum):
    """
    Base bitmap RGB values.

    Colors are drawn on the bitmap in the order they appear here.
    Meaning the first enum is drawn on the bottom-most layer and the last is drawn on the top-most layer.
    """
    Water = (0, 138, 255)
    DarkGrass = (90, 100, 35)
    MediumGrass = (117, 117, 47)
    LightGrass = (145, 135, 60)
    Dirt = (120, 70, 20)
    DirtGrass = (80, 55, 20)
    GravelDirt = (140, 70, 15)
    Sand = (210, 200, 160)
    LightAsphalt = (165, 160, 140)      # sidewalk/cement pavement
    MediumAsphalt = (120, 120, 120)
    DarkAsphalt = (100, 100, 100)       # main roads
    LightPothole = (130, 120, 120)
    DarkPothole = (110, 100, 100)


class VMColor(Enum):
    """
    Vegetation bitmap RGB values.

    Colors are drawn on the bitmap in the order they appear here.
    Meaning the first enum is drawn on the bottom-most layer and the last is drawn on the top-most layer.
    """
    Nothing = (0, 0, 0)
    DenseForest = (255, 0, 0)
    DenseTreesAndGrass = (200, 0, 0)
    TreesAndGrass = (127, 0, 0)
    FirTreesAndGrass = (64, 0, 0)
    MainlyGrassSomeTrees = (0, 128, 0)
    LightLongGrass = (0, 255, 0)
    BushesGrassFewTrees = (255, 0, 255)
    DeadCorn1 = (255, 128, 0)
    DeadCorn2 = (220, 100, 0)


# TODO: Zombie Spawn Map
#   The zombie spawn map is in greyscale, where black (0,0,0) represents no zombies
#   and white (255,255,255) represents the max amount of zombies.
#   I believe greyscale colors must have the exact same values for all (r,g,b).
#   I imagine an enum for these colors is unnecessary


# OPENSTREETMAP RELATED

class HighwayType(Enum):
    """
    All OpenStreetMap highway types.

    Reference: https://wiki.openstreetmap.org/wiki/Key:highway
    """

    # Roads (main tags for the road network)
    MOTORWAY = "motorway"
    TRUNK = "trunk"
    PRIMARY = "primary"
    SECONDARY = "secondary"
    TERTIARY = "tertiary"
    UNCLASSIFIED = "unclassified"
    RESIDENTIAL = "residential"

    # Link Roads
    MOTORWAY_LINK = "motorway_link"
    TRUNK_LINK = "trunk_link"
    PRIMARY_LINK = "primary_link"
    SECONDARY_LINK = "secondary_link"
    TERTIARY_LINK = "tertiary_link"

    # Special road types
    LIVING_STREET = "living_street"
    SERVICE = "service"
    PEDESTRIAN = "pedestrian"
    TRACK = "track"
    BUS_GUIDEWAY = "bus_guideway"
    ESCAPE = "escape"
    RACEWAY = "raceway"
    ROAD = "road"   # road of unknown type
    BUSWAY = "busway"

    # Paths
    FOOTWAY = "footway"
    BRIDLEWAY = "bridleway"
    STEPS = "steps"
    CORRIDOR = "corridor"
    PATH = "path"
    VIA_FERRATA = "via_ferrata"

    # When sidewalk/crosswalk is tagged as a separate way (key=footway)
    SIDEWALK = "sidewalk"
    CROSSING = "crossing"
    TRAFFIC_ISLAND = "traffic_island"

    # When sidewalk (or pavement) is tagged on the main roadway (key=sidewalk)
    # TODO: both | left | right | no
    # Specifies that the highways has sidewalks on both sides, on one side or no sidewalk at all

    # When cycleway is drawn as its own way
    CYCLEWAY = "cycleway"

    # TODO: continued at https://wiki.openstreetmap.org/wiki/Key:highway
