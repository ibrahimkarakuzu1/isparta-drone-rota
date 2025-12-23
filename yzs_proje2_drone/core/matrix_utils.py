# c# core/matrix_utils.py
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 
    return c * r

def get_distance_matrix(locations):
    city_names = list(locations.keys())
    n = len(city_names)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j: matrix[i][j] = 0
            else:
                coords_i = locations[city_names[i]]
                coords_j = locations[city_names[j]]
                matrix[i][j] = haversine(coords_i[1], coords_i[0], coords_j[1], coords_j[0])
    return matrix, city_names