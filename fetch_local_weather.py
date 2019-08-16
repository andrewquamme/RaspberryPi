from requests import get
import json
from pprint import pprint
from haversine import haversine


def find_closest():
    smallest = 20036
    for station in all_stations:
        station_lat = station['weather_stn_lat']
        station_lon = station['weather_stn_long']
        distance = haversine(my_lat, my_lon, station_lat, station_lon)
        if distance < smallest:
            smallest = distance
            closest_station = station['weather_stn_id']
    return closest_station

stations = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'
weather = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getlatestmeasurements/'

my_lat = 32.2328
my_lon = -110.9535

all_stations = get(stations).json()['items']

closest_stn = find_closest()

weather += str(closest_stn)

my_weather = get(weather).json()['items']
pprint(my_weather)
