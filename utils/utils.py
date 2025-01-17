import math

def calc_lat_lon_range(lat, lon, distance_km):
    KM_PER_DEGREE = 111

    delta_lat = distance_km / KM_PER_DEGREE
    delta_lon = distance_km / (KM_PER_DEGREE * math.cos(math.radians(lat)))

    lat_min, lat_max = lat - delta_lat, lat + delta_lat
    lon_min, lon_max = lon - delta_lon, lon + delta_lon

    return lat_min, lat_max, lon_min, lon_max