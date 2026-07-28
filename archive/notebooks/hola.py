import folium
from folium import Choropleth, LayerControl, Marker, GeoJson
from folium.plugins import Fullscreen

# Crear mapa centrado en Providencia
m = folium.Map(location=[-33.43, -70.61], zoom_start=14, tiles="CartoDB positron")
Fullscreen().add_to(m)

# Agregar tráfico como líneas coloreadas por velocidad
for _, row in trafico.iterrows():
    coords = list(row['geometry'].coords)
    color = 'green' if row['speed'] > 30 else 'orange' if row['speed'] > 15 else 'red'
    folium.PolyLine(
        coords,
        color=color,
        weight=4,
        opacity=0.8,
        tooltip=f"Velocidad: {row['speed']} km/h"
    ).add_to(m)

# Guardar como HTML
m.save("mapa_trafico_providencia.html")