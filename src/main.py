
import generate_map
import input
from classes.Optimizer import Optimizer

# TODO
#   [x] Basic map generation functionality
#   [x] Refactor this into a map object
#   [x] Upload arbitrary real location using map
#   [x] Separate Overpass query from rest of map generation
#   [ ] Store/load Overpass query data
#   [x] Get user input for map name, coordinates, etc
#   [x] Convert map data to ways
#   [x] Convert ways into a network of vertices (is this even necessary?)
#   [ ] Draw polygons
#   [ ] Water
#   [ ] Straighten ways
#   [ ] Veg map (directly depends on a completed base map)
#   [ ] Zombie spawn map (stretch goal)
#   [ ] Foraging zones (stretch goal)
#   [ ] Fill in houses (super stretch goal)
#   [ ] Implement GUI (super duper stretch goal)


def main():
    # get data for map
    map_data = input.select_mode()

    # generate initial map from data
    pz_map = generate_map.generate(map_data)

    node_count = 0
    for way in pz_map.ways:
        node_count += len(way.nodes)
    print(f"Node count before: {node_count}")

    # optimize map
    optimizer = Optimizer(pz_map)
    optimizer.preprocess()

    node_count = 0
    for way in pz_map.ways:
        node_count += len(way.nodes)
    print(f"Node count after: {node_count}")

    pz_map.draw_ways()


if __name__ == '__main__':
    main()
