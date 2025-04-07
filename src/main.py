
import generate_map
import input

# TODO
#   [x] Basic map generation functionality
#   [x] Refactor this into a map object
#   [x] Upload arbitrary real location using map
#   [x] Separate Overpass query from rest of map generation
#   [ ] Store/load Overpass query data
#   [x] Get user input for map name, coordinates, etc
#   [x] Convert map data to ways
#   [ ] Convert ways into a network of vertices (is this even necessary?)
#   [ ] Draw polygons
#   [ ] Water
#   [ ] Straighten ways
#   [ ] Veg map (directly depends on a completed base map)
#   [ ] Zombie spawn map (stretch goal)
#   [ ] Foraging zones (stretch goal)
#   [ ] Fill in houses (super stretch goal)
#   [ ] Implement GUI (super duper stretch goal)


def main():
    map_data = input.select_mode()
    pz_map = generate_map.generate(map_data)


if __name__ == '__main__':
    main()
