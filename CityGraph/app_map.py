import plotly.express as px
df = px.data.gapminder().query("year == 2007")
fig = px.line_geo(df, locations="iso_alpha",
                  color="continent", # "continent" is one of the columns of gapminder
                  projection="orthographic")
fig.show()
exit()

import geojson
import plotly.express as px

filepath = '../data/22_BCN/car_agent_paths_4326.geojson'
with open(filepath, 'r') as geojson_file:
    agent_path = geojson.load(geojson_file)


fcRailroad = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -105.0913953781128,
                        40.49348616373978
                    ],
                    [
                        -105.0906443595885,
                        40.49508532104079
                    ],
                    [
                        -105.0863313674927,
                        40.502411585011934
                    ]
                ]
            }
        }
    ]
}

#fig = px.line_mapbox(agent_path, lat="lat", lon="lon", color="State", zoom=3, height=300)
print(type(agent_path))
print(agent_path)
#fig = px.line_geo(geojson=geojson.dumps(agent_path))
fig = px.line_geo(geojson=fcRailroad)

#fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=4, mapbox_center_lat = 41,
#    margin={"r":0,"t":0,"l":0,"b":0})

fig.show()