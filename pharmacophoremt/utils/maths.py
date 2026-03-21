import numpy as np
from pharmacophoremt import pyunitwizard as puw

def ring_normal(indices, coords, centroid):
    """Calculate the normal vector of the plane defined by an aromatic ring."""
    vec_1 = coords[indices[0]] - centroid
    vec_2 = coords[indices[1]] - centroid
    normal = np.cross(puw.get_value(vec_1), puw.get_value(vec_2))
    norm = np.linalg.norm(normal)
    if norm < 1e-6:
        return np.array([0.0, 0.0, 1.0])
    return normal / norm

def point_projection(normal, plane_point, point):
    """Returns the projection of a point into a plane."""
    vec = point - plane_point
    dist = np.dot(puw.get_value(vec), normal)
    return point - dist * normal * puw.get_unit(point)

def angle_between_normals(normal_1, normal_2):
    """Compute the angle between the normals of two planes in degrees."""
    denominator = np.linalg.norm(normal_1) * np.linalg.norm(normal_2)
    if denominator < 1e-6:
        return 0.0
    dot_prod = np.clip(np.dot(normal_1, normal_2) / denominator, -1.0, 1.0)
    angle = np.degrees(np.arccos(dot_prod))
    if angle > 90:
        angle = 180 - angle
    return angle

def nearest_bins(num, bin_size):
    """Return the nearest bins for a given number."""
    if num % 1 <= 0.5:
        low_bin = np.floor(num - bin_size)
    else:
        low_bin = np.ceil(num - bin_size)
    return low_bin, low_bin + 1

def points_distance(coords_1, coords_2):
    """Returns the Euclidean distance between two points."""
    diff = puw.get_value(coords_1) - puw.get_value(coords_2)
    dist = np.sqrt(np.sum(diff**2))
    return puw.quantity(dist, puw.get_unit(coords_1))
