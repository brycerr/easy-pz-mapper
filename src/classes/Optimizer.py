
import math

class Optimizer:
    def __init__(self):
        self.iterations = -1


def preprocess(map_obj):
    for way in map_obj.ways:
        for node in way.nodes:
            return


def ramer_douglas_puecker(points, epsilon):
    """
    Given a curve (list of points connected by edges), this algorithm decimates the te curve into a similar curve.
    This reduces the number of edges in the curve, decreasing the work needed to be done by the optimizer.

    This function is based on https://karthaus.nl/rdp/
    """

    # find the point with the maximum distance
    dist_max = 0
    index = 0
    end = len(points)
    for i in range(2, (end - 1)):
        dist = perpendicular_distance()     # TODO
        if dist > dist_max:
            index = i
            dist_max = dist

    results = []
    # if max distance is greater than epsilon, recursively simplify
    if dist_max > epsilon:
        rec_results_1 = ramer_douglas_puecker(points[range(1, index)], epsilon)
        rec_results_2 = ramer_douglas_puecker(points[range(index, end)], epsilon)

        # build the results list
        rec_results_2.pop(0)
        results = rec_results_1.append(rec_results_2)
    else:
        results = [points[1], points[end]]

    return results


def perpendicular_distance():
    # TODO
    return -1
