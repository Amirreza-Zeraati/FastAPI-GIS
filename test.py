import folium
import folium.raster_layers
import sqlite3
import geopandas as gpd

connection = sqlite3.connect("gpsdb.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM locations")
t = cursor.fetchall()

print(t)

# db = [[36.21065316666667, 57.703376166666665],
#       [38, 60],
#       [38, 57],
#       [33, 59]]

colors = ['red', 'blue', 'green', 'black']
msg = ['red', 'blue', 'green', 'black']

loc = folium.Map(location=[36.105868759971926, 57.454934234499085],
                 max_bounds=True,
                 min_lat=29,
                 min_lon=56,
                 max_lat=38.5,
                 max_lon=63,
                 zoom_start=6.5,
                 min_zoom=6.5)

# for i in t:
#     if i[1] is not None:
#         folium.Marker([i[1], i[2]], popup=folium.Popup("slam", parse_html=True, max_width=100),
#         icon=folium.Icon(color=colors[i[4]-1])).add_to(loc)

folium.Marker([36, 57], popup=folium.Popup("slam", parse_html=True, max_width=100)).add_to(loc)

folium.LayerControl().add_to(loc)
loc.save('I:\Work\GPS/application/templates\map2.html')


gdf = gpd.read_file("ostan\REGIONS_shp.shx")

m = folium.Map(location=[36, 57],
                zoom_start=7,
                min_zoom=7,
                max_bounds=True,
                min_lat=33,    # from down
                min_lon=56,    # from left
                max_lat=38,    # from up
                max_lon=63)    # from right

folium.GeoJson(gdf,
               name = 'Shapefile Layer',
               style_function = lambda feature: {
                    "fillColor": "none",
                    "color": "black",
                    "weight": 2 },
                zoom_on_click=True).add_to(m)

folium.Marker([36.210664333333334, 57.703338], icon=folium.Icon(color='red')).add_to(m)
folium.LayerControl().add_to(m)
m.save('application/templates/map.html')