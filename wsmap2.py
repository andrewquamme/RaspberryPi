from requests import get
import webbrowser
import folium
import os
import html


def c_to_f(temp):
    return temp*(9/5)+32


def colorgrad(minimum, maximum, val):
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2*(val-minimum)/(maximum-minimum)
    b = int(max(0, 255*(1-ratio)))
    g = int(max(0, 255*(ratio-1)))
    r = 255-b-g
    hex = '#%02x%02x%02x' % (r, g, b)
    return hex


def main():
    url = 'https://apex.oracle.com/pls/apex/raspberrypi/weatherstation/getalllastmeasurement'
    station_data = get(url).json()

    temps = []
    tmax = 0.0
    tmin = 100.0
    lats = [data['weather_stn_lat'] for data in station_data['items']]
    lons = [data['weather_stn_long'] for data in station_data['items']]
    wsnames = [html.escape(station['weather_stn_name']) for station in station_data['items']]

    for data in station_data['items']:
        if 'ambient_temp' in data:
            t = data['ambient_temp']
            if t > 50 or t < -30:
                t = 0
            if t > tmax:
                tmax = t
            if t < tmin:
                tmin = t
            temps.append(str(t))

    ws_map = folium.Map(location=[32, -110], zoom_start=4)
    for i in range(len(lats)-1):
        col = colorgrad(tmin, tmax, float(temps[i]))
        folium.CircleMarker([lats[i], lons[i]],
                            radius=5,
                            popup=wsnames[i]+':'+temps[i],
                            fill_color=col).add_to(ws_map)

    CWD = os.getcwd()
    ws_map.save('wsmap2.html')


main()
