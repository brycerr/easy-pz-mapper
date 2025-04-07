
import math


class Optimizer:
    def __init__(self, pz_map):
        self.pz_map = pz_map

    def preprocess(self):
        print("Preprocessing...")
        # use the Ramer-Douglas-Peucker algorithm to decimate each way into a similar way using less nodes (if possible)
        epsilon = 1.0
        for way in self.pz_map.ways:
            way.nodes = rdp(way.nodes, epsilon)
        print("Preprocessing complete.")


def rdp(nodes, epsilon):
    """
    Simplify a way using the Ramer-Douglas-Peucker algorithm.
    """
    if len(nodes) < 3:
        return nodes

    # find the point with the maximum distance
    start, end = nodes[0], nodes[-1]
    max_dist = 0
    index = 0
    for i in range(1, len(nodes) - 1):
        dist = point_line_distance(nodes[i], start, end)
        if dist > max_dist:
            index = i
            max_dist = dist

    # if max distance is greater than epsilon, recursively simplify
    if max_dist > epsilon:
        left = rdp(nodes[:index + 1], epsilon)
        right = rdp(nodes[index:], epsilon)

        # combine results, avoiding duplicate point at the split
        return left[:-1] + right
    else:
        return [start, end]


def point_line_distance(node, start, end, tol=1e-9):
    """
    Calculate the perpendicular distance from a point to a line segment.

    tol: used to determine if two floats are the same
    """
    if math.dist(start.get_point(), end.get_point()) < tol:
        return math.dist(node.get_point(), start.get_point())

    x, y = node.get_point()
    x1, y1 = start.get_point()
    x2, y2 = end.get_point()

    # project point onto line segment
    numerator = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
    denominator = math.hypot(x2 - x1, y2 - y1)
    return numerator / denominator


# for testing purposes
if __name__ == "__main__":
    print("Ramer-Douglas-Peucker Test")
    test_points = [(0, 0), (1, 0.1), (2, -0.1), (3, 5), (4, 6), (5, 7)]
    test_epsilon = 1
    print(f"Points: {test_points}")
    print(f"Epsilon: {test_epsilon}")

    simplified = rdp(test_points, test_epsilon)
    print(f"Simplified: {simplified}")
