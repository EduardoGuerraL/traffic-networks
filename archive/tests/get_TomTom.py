import osmnx as ox
import requests
import json

# 1. Define la ciudad y exporta el polígono
ciudad = "Santiago, Chile"
gdf = ox.geocode_to_gdf(ciudad)
gdf.to_file("santiago.geojson", driver="GeoJSON")

# 2. Define parámetros de la consulta
api_key = "DtIhgPz485o77dq0S8emJKsyOA1e16xT"  # reemplaza con tu clave
url = f"https://api.tomtom.com/trafficstats/1/areaanalysis?key={api_key}"

# 3. Carga el polígono como JSON
with open("santiago.geojson") as f:
    geojson = json.load(f)

# 4. Crea el cuerpo de la petición
body = {
    "geometry": geojson['features'][0]['geometry'],
    "dateRange": {
        "startDate": "2024-01-01",
        "endDate": "2024-01-31"
    },
    "timeRange": {
        "startTime": "07:00",
        "endTime": "10:00"
    },
    "daysOfWeek": ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY"],
    "dataType": "HISTORICAL",
    "outputFormat": "JSON"
}

# 5. Enviar la solicitud
response = requests.post(url, json=body)

# 6. Mostrar resultado
if response.status_code == 200:
    print("Consulta enviada exitosamente.")
    print("Resultado:", response.json())
else:
    print("Error:", response.status_code, response.text)
