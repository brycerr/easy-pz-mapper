import decimal
import math
import re


def sanitize_input(input_str):
    """Returns a string that is a valid windows filepath."""
    return re.sub(r"[^\w\-. ]+$", "", input_str)


def haversine_distance(a, b):
    """Calculates distance between two coordinates a and b."""
    r = 6371    # radius of Earth (km)
    p = math.pi / 180

    lat1, lon1 = float(a[0]), float(a[1])
    lat2, lon2 = float(b[0]), float(b[1])

    # distance between latitudes and longitudes
    d_lat = (lat2 - lat1) * p
    d_lon = (lon2 - lon1) * p

    temp = 0.5 - (math.cos(d_lat) / 2) + math.cos(lat1 * p) * math.cos(lat2 * p) * ((1 - math.cos(d_lon)) / 2)

    return 2 * r * math.asin(math.sqrt(temp))
