import folium
import pandas as pd

#Datos
#Volcanes:
url = "https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv"

chunk_size = 1000 
chunks = []

for chunk in pd.read_csv(url, encoding='latin1', chunksize=chunk_size):
    chunks.append(chunk)

data = pd.concat(chunks, axis=0)

#Funciones
def time_translator(time):
    if time == "D1":
        return "> 1963"
    elif time == "D2":
        return "1900 - 1963"
    elif time == "D3":
        return "Siglo 19"
    elif time == "D4":
        return "Siglo 18"
    elif time == "D5":
         return"Siglos 16-17" 
    elif time == "D6":
          return "Siglo 1-15"
    elif time == "D7":
        return "AC"
    else: 
        return "Unknown/Uncertain"
def color_selector(Time):
    if time == "D1" or time == "D2": # Siglo 20
        return 'red'
    elif time == "D3": #Siglo 19
        return 'orange'
    elif time == "D4": #Siglo 18
        return 'green'
    elif time == "D5" or time == "D6": #Siglos 1-17
        return 'lightblue'    
    elif time == "D7": #AC
        return 'darkblue'
    else: 
        return 'black'    



lat = list(data["Latitude"])
lon = list(data["Longitude"])
names = data["Volcano Name"] + ", " + data["Country"]
names = names.tolist()  # Convierte la Series a una lista
Erupt_time = list(data["Last Known"])


    



mapP = folium.Map(location=[41.4766700, 2.0833300], zoom_start=1)

fgP = folium.FeatureGroup(name="Poblacion")

fgP.add_child(folium.GeoJson(data = open('world.json','r',encoding= 'utf-8-sig').read(),style_function= lambda x: {'fillColor': 'green' if x['properties']['POP2005'] < 20000000 else 'orange' 
                                                                                                                 if 20000000 <= x['properties']['POP2005'] < 75000000 else 'red'}))
fgV = folium.FeatureGroup(name = "Volcanes")

for lt, ln, name, time in zip(lat, lon, names, Erupt_time):
    fgV.add_child(folium.CircleMarker(location=[lt, ln],radius = 5, popup=name +  "\n Ultima Erupcion: " + time_translator(time),color = color_selector(time), fill = True, fill_color = color_selector(time)))

mapP.add_child(fgP)
mapP.add_child(fgV)  
mapP.add_child(folium.LayerControl())

# Añadir leyenda personalizada para volcanes
legend_volcano = '''
<div style="position: fixed;
            bottom: 50px; left: 50px; width: 180px; height: 130px;
            border:1px solid grey; z-index:9999; font-size:12px;
            background-color:white;
            padding: 10px;
            ">
            &nbsp; <b>Leyenda Volcanes</b> <br>
            &nbsp; <i class="fa fa-circle fa-1x" style="color:red"></i> > 1963 <br>
            &nbsp; <i class="fa fa-circle fa-1x" style="color:orange"></i> 1900 - 1963 <br>
            &nbsp; <i class="fa fa-circle fa-1x" style="color:green"></i> Siglo 18 <br>
            &nbsp; <i class="fa fa-circle fa-1x" style="color:lightblue"></i> Siglos 16-17 <br>
            &nbsp; <i class="fa fa-circle fa-1x" style="color:darkblue"></i> AC <br>
            &nbsp; <i class="fa fa-circle fa-1x" style="color:black"></i> Unknown/Uncertain <br>
</div>
'''

# Añadir leyenda personalizada para población
legend_population = '''
<div style="position: fixed;
            bottom: 50px; left: 250px; width: 200px; height: 100px;
            border:1px solid grey; z-index:9999; font-size:12px;
            background-color:white;
            padding: 10px;
            ">
            &nbsp; <b>Leyenda Poblacion</b> <br>
            &nbsp; <i class="fa fa-square fa-lg" style="color:green"></i> < 20.000.000 <br>
            &nbsp; <i class="fa fa-square fa-lg" style="color:orange"></i> 20.000.000 - 75.000.000 <br>
            &nbsp; <i class="fa fa-square fa-lg" style="color:red"></i> > 75.000.000 <br>
</div>
'''

mapP.get_root().html.add_child(folium.Element(legend_volcano))
mapP.get_root().html.add_child(folium.Element(legend_population))

mapP.save("MAPA_Volcanes_Poblacion.html")

