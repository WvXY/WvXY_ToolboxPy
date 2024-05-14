import numpy as np


# https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
def line_intersection(l1, l2):
    """
    :param l1: line 1[2x2] = [[x1, y1], [x2, y2]]
    :param l2: line 2[2x2] = [[x1, y1], [x2, y2]]
    :return: intersection point
    """
    r, s = l1[1] - l1[0], l2[1] - l2[0]
    p, q = l1[0], l2[0]
    rxs, gpxr = np.cross(r, s), np.cross(q - p, r)

    if rxs == 0:
        if qpxr == 0:  # collinear
            return None
        else:  # parallel
            return None
    else:
        t = np.cross(q - p, s) / rxs
        u = qpxr / rxs
        if 0 <= t <= 1 and 0 <= u <= 1:  # intersection is within the segments
            return p + t * r
        else:  # intersection is outside the segments
            return None


if __name__ == "__main__":
    l1 = np.array([[0, 0], [3, 3]])
    l2 = np.array([[0, 3], [3, 0]])

    k = line_intersection(l1, l2)
    if k.all() is not None:
        print(k)
