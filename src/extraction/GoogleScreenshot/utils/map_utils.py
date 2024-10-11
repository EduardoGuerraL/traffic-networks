def generate_map_html(api_key, coords, zoom, include_traffic, output_file):
    traffic_layer = "const trafficLayer = new google.maps.TrafficLayer();" if include_traffic else ""
    traffic_set = "trafficLayer.setMap(map);" if include_traffic else ""

    html_content = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>Mapa de tráfico vehicular</title>
    <script src="https://maps.googleapis.com/maps/api/js?key={api_key}"></script>
    <script>
      function initMap() {{
        const rectangulo = new google.maps.LatLngBounds(
            new google.maps.LatLng({coords['southwest']['lat']}, {coords['southwest']['lng']}),
            new google.maps.LatLng({coords['northeast']['lat']}, {coords['northeast']['lng']})
        );
        const map = new google.maps.Map(document.getElementById("map"), {{
          center: rectangulo.getCenter(),
          zoom: {zoom},
          mapTypeId: "roadmap",
          styles: [
            {{
              featureType: "poi",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "transit",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "road",
              elementType: "labels.icon",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "road.arterial",
              elementType: "labels.icon",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "road",
              elementType: "labels.text.fill",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "road",
              elementType: "labels.text.stroke",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "road",
              elementType: "geometry.stroke",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "administrative",
              elementType: "labels",
              stylers: [{{ visibility: "off" }}],
            }},
            {{
              featureType: "water",
              stylers: [{{ visibility: "on" }}],
            }},
          ],
        }});
        {traffic_layer}
        {traffic_set}
        map.fitBounds(rectangulo);
      }}
    </script>
    <style>
      #map {{
        height: 100%;
      }}
      html,
      body {{
        height: 100%;
        margin: 0;
        padding: 0;
      }}
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>
      initMap();
    </script>
  </body>
</html>
"""
    with open(output_file, 'w') as file:
        file.write(html_content)
