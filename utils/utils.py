import math

def calcLatLonRange(lat, lon, distance_km):
    km_per_degree = 111

    delta_lat = distance_km / km_per_degree
    delta_lon = distance_km / (km_per_degree * math.cos(math.radians(lat)))

    lat_min, lat_max = lat - delta_lat, lat + delta_lat
    lon_min, lon_max = lon - delta_lon, lon + delta_lon

    return lat_min, lat_max, lon_min, lon_max