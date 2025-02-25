from enum import Enum


class BMColor(Enum):
    """Base map RGB values."""
    DarkGrass = (90, 100, 35)
    MediumGrass = (117, 117, 47)
    LightGrass = (145, 135, 60)
    Sand = (210, 200, 160)
    LightAsphalt = (165, 160, 140)      # sidewalk/cement pavement
    DarkAsphalt = (100, 100, 100)       # main roads
    MediumAsphalt = (120, 120, 120)
    GravelDirt = (140, 70, 15)
    Dirt = (120, 70, 20)
    DirtGrass = (80, 55, 20)
    DarkPothole = (110, 100, 100)
    LightPothole = (130, 120, 120)
    Water = (0, 138, 255)


class VMColor(Enum):
    """Vegetation map RGB values."""
    DenseForest = (255, 0, 0)
    DenseTreesAndGrass = (200, 0, 0)
    TreesAndGrass = (127, 0, 0)
    FirTreesAndGrass = (64, 0, 0)
    MainlyGrassSomeTrees = (0, 128, 0)
    LightLongGrass = (0, 255, 0)
    BushesGrassFewTrees = (255, 0, 255)
    DeadCorn1 = (255, 128, 0)
    DeadCorn2 = (220, 100, 0)
    Nothing = (0, 0, 0)
