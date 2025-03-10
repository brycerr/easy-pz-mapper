import os

import generate_map

# TODO
#   [x] Basic map generation functionality
#   [x] Refactor this into a map object
#   [ ] ...
#   [x] Upload arbitrary real location using map
#   [ ] Get user input for map name, coordinates, etc
#   [x] Convert map data to ways
#   [ ] Convert ways into a network of vertices
#   [ ] Draw polygons
#   [ ] Water
#   [ ] Straighten ways
#   [ ] Foraging zones
#   [ ] Fill in houses
#   [ ] ...


def main():
    pz_map = generate_map.generate()


if __name__ == '__main__':
    main()
