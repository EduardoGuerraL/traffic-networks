# capture/map_generator.py

def generate_map_html(api_key, coords, zoom, include_traffic, output_file):
    traffic_layer = "const trafficLayer = new google.maps.TrafficLayer();" if include_traffic else ""
    traffic_set = "trafficLayer.setMap(map);" if include_traffic else ""

    html_content = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Mapa de tráfico</title>
    <script src="https://maps.googleapis.com/maps/api/js?key={api_key}"></script>
    <script>
      function initMap() {{
        const bounds = new google.maps.LatLngBounds(
            new google.maps.LatLng({coords['southwest']['lat']}, {coords['southwest']['lng']}),
            new google.maps.LatLng({coords['northeast']['lat']}, {coords['northeast']['lng']})
        );
        const map = new google.maps.Map(document.getElementById("map"), {{
          center: bounds.getCenter(),
          zoom: {zoom},
          mapTypeId: "roadmap"
        }});
        {traffic_layer}
        {traffic_set}
        map.fitBounds(bounds);
      }}
    </script>
    <style>
      html, body, #map {{
        height: 100%;
        margin: 0;
        padding: 0;
      }}
    </style>
  </head>
  <body onload="initMap()">
    <div id="map"></div>
  </body>
</html>
"""
    with open(output_file, 'w') as f:
        f.write(html_content)
