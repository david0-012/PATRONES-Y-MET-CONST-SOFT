from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Lugares
import folium
from folium.plugins import FastMarkerCluster

def home(request):
    locations_list = Lugares.objects.all()
    paginator = Paginator(locations_list, 4) # Muestra 4 ubicaciones por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    initialMap = folium.Map(location=[4.662426,-74.110292], zoom_start=12)

    # Creamos los marcadores para todas las ubicaciones
    for location in locations_list:
        coordinates = (location.lat, location.lng)
        folium.Marker(coordinates, popup= location.name).add_to(initialMap)

    context = {'map':initialMap._repr_html_(), 'page_obj':page_obj}
    return render(request, 'mapa.html', context)