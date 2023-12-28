#imported folium, pandas, and random
from cgitb import html
from concurrent.futures.process import _MAX_WINDOWS_WORKERS
import folium, pandas, random, webbrowser, os
my_map = folium.Map(location=[41.4925, -99.9018], zoom_start=5, tiles="openstreetmap")

#color generator, generates colors
def color_picker(): #parameter may be elev (see below)
    x = random.randint(0,17)
    possible_colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred','lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    color = possible_colors[x]
    return color
    #if requiring color-coded generator based on volcano elevation
    #if elev < 1000:
    #   return possible_colors[2]
    #elif 1000 < elev < 3000:
    #   return possible_colors[1]
    #else:
    #   return possible_colors[0]

#getting the data; see Volcanoes.txt
data = pandas.read_csv("../Resources/Volcanoes.txt")
latitude = list(data["LAT"])
longitude = list(data["LON"])

#the text included in the popup from Volcanoes.txt
name = list(data["NAME"])
location = list(data["LOCATION"])
status = list(data["STATUS"])
elevation = list(data["ELEV"])
type_volcano = list(data["TYPE"])
timef = list(data["TIMEFRAME"])
fg = folium.FeatureGroup(name="Volcano Information")

#for-loop to include all the information in the pop-ups.
for x, y, z, a, b, c, d, e in zip(latitude, longitude, name, location, status, elevation, type_volcano, timef):
    popup = folium.Popup("Information: \n  Name: {} \n  Location: {} \n  Status: {} \n  Elevation: {} m  \n Volcano Type: {} \n Time Frame: {} ".format(str(z), str(a), str(b), str(c), str(d), str(e)), max_width=500)
    fg.add_child(folium.Marker(location=[x, y], radius=6, popup=popup, parse_HTML = True, icon=folium.Icon(color=color_picker())))
    my_map.add_child(fg)
    my_map.save("..\\HTML\\volcanoInformation.html")

#adding the population layer to the map; see world-two.json
fg2 = folium.FeatureGroup(name="World Population")
fg2.add_child(folium.GeoJson(data=open("../Resources/world_two.json", "r", encoding="utf-8-sig").read(),
                             style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 50000000
else 'orange' if 50000000 <= x['properties']['POP2005'] < 100000000 else 'red', 'color':'black','weight':0,'dashArray':'5, 5'}, smooth_factor=0.0005)) 
my_map.add_child(fg2)
my_map.save("..\\HTML\\volcanoInformation.html")


#add layer control 
my_map.add_child(folium.LayerControl('topright'))
my_map.save("..\\HTML\\volcanoInformation.html")

#Open App
filename = "file:///"+os.getcwd()+"/" + "../HTML/volcanoInformation.html"
webbrowser.open_new_tab(filename)