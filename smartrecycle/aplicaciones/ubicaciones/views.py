


from django.shortcuts import render
from .models import Lugares
import folium
from folium.plugins import FastMarkerCluster

def home(request):
    # Recupero todas las sucursales
    locations = Lugares.objects.all()

    # Defino el mapa
    initialMap = folium.Map(location=[4.662426,-74.110292], zoom_start=12)

    # Creamos el Clustering de los marcadores
    #latitudes = [location.lat for location in locations]
    #longitudes = [location.lng for location in locations]
    #popups = [location.name for location in locations]
    #FastMarkerCluster(data=list(zip(latitudes, longitudes, popups))).add_to(initialMap)

    # Creamos los marcadores
    for location in locations:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup= location.name).add_to(initialMap)

    context = {'map':initialMap._repr_html_(), 'locations':locations}
    return render(request, 'mapa.html', context)