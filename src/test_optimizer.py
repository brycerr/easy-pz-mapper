
import math

ALLOWED_ANGLES = [0, 45, 90, 135, 180, 225, 270, 315]


def angle_between(p1, p2):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    return math.degrees(math.atan2(dy, dx)) % 360


def snap_to_octilinear(angle):
    return min(ALLOWED_ANGLES, key=lambda a: abs((angle - a + 180) % 360 - 180))


def move_point(origin, angle_deg, length):
    angle_rad = math.radians(angle_deg)
    dx = length * math.cos(angle_rad)
    dy = length * math.sin(angle_rad)
    return origin[0] + dx, origin[1] + dy


def optimize_map_octilinear(pz_map):
    visited = set()

    for way in pz_map.ways:
        nodes = way.nodes
        if len(nodes) < 2:
            continue

        # keep first node fixed
        p1 = nodes[0].get_point()
        for i in range(1, len(nodes)):
            if nodes[i] in visited:
                continue  # don't move already fixed nodes

            p2 = nodes[i].get_point()
            length = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
            angle = angle_between(p1, p2)
            snapped_angle = snap_to_octilinear(angle)
            new_p2 = move_point(p1, snapped_angle, length)

            # update node position
            nodes[i].x = new_p2[0]
            nodes[i].y = new_p2[1]
            visited.add(nodes[i])
            p1 = new_p2

            # print(f"Moved node {nodes[i].id} from {p2} to {new_p2}")
