from requests import get
import json
import folium
import os
import webbrowser
import html

url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getallstations'

stations = get(url).json()
lons = [station['weather_stn_long'] for station in stations['items']]
lats = [station['weather_stn_lat'] for station in stations['items']]
wsnames = [html.escape(station['weather_stn_name']) for station in stations['items']]

ws_map = folium.Map(location=[32, -110], zoom_start=6)

for i in range(len(lats)):
    folium.Marker([lats[i],
                   lons[i]],
                  icon=folium.Icon(icon='cloud', color='green'),
                  popup=wsnames[i]).add_to(ws_map)

CWD = os.getcwd()
ws_map.save('wsmap1.html')
# webbrowser.open_new('file://'+CWD+'/'+'wsmap1.html')
