# Traffic Networks
## _Análisis de congestión vehicular con teoría de redes complejas_

Este proyecto busca **estudiar la congestión vehicular en ciudades a partir de datos de Google Maps y teoría de redes complejas**.  
El caso de estudio inicial es **Punta Arenas (Chile)**, pero la metodología es adaptable a cualquier ciudad.

---

## Objetivo
Analizar si las métricas de centralidad en redes urbanas (closeness, betweenness, eigenvector, etc.)  
se correlacionan con los niveles reales de congestión vehicular.

---

## Flujo de trabajo

1. **Obtención de datos**
   - Imágenes de tráfico vehicular descargadas desde la **API de Google Maps** usando src\extraction.
      - El zoom de Google Maps nos entrega diferentes categorías de calles (principal, secundaria, carretera, etc), debo buscar cuales son las que nos mostró en este caso.
   - Imágenes tomadas cada **15 minutos durante ~2 meses**. Esto nos dió un total de 2908 imágenes, que se encuentran en data/raw, con la notación: ańo-mes-dia_hora:min.png

2. **Construcción de la red urbana**
   - Inicialmente: creación **manual** de la red a partir de la dirección de calles.
      - Se hizo una interfaz que sea fácil de usar para el usuario. (tal vez deba haber una documentación explicando a detalle)
   - En desarrollo: **automatización con OSMnx**

3. **Procesamiento de imágenes**
   - Cada imagen contiene colores según el tráfico: verde, amarillo, rojo, rojo ocuro.
   - Obtenemos el valor de tráfico que equivale para cada nodo de la red creada en la seccion 2 en cada instante de tiempo. 
      -Aqui podemos usar distintos radios de covertura(poner imagen)
      -También mostrar como se obtiene el valor de tráfico para la red dual.
   - Se calcula un **promedio de intensidad de tráfico por nodo** en cada instante de tiempo (tomamos solo dias de semana).
   - Se genera una **escala lineal de tráfico** (0 = fluido, 1 = muy congestionado).

4. **Análisis de redes complejas**
   - Se calculan métricas: closeness, betweenness, eigenvector centrality.
   - Se comparan con los valores de tráfico en el tiempo.

5. **Resultados**
   - Se observan correlaciones más fuertes entre **ciertas métricas de centralidad**  
     y el tráfico vehicular en **horas de alta congestión**.

---

## Ejemplo de resultados (aun no lo pondré)

- Gráficos comparando la evolución temporal de la congestión y las centralidades.
- Mapas urbanos coloreados según el grado de centralidad vs congestión observada.

![Imagen de resultados][]

---

## Tecnologías

- **Python 3.12**
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `networkx`, `osmnx`
- `opencv` (para procesamiento de imágenes)
---

## Cómo usar el proyecto

```bash
# Clonar el repositorio
git clone https://github.com/EduardoGuerraL/CellAuToTraffic
cd traffic-networks

# Instalar dependencias
pip install -r requirements.txt

# Explorar los notebooks
jupyter notebook notebooks/ (aún en contrucción)
'''

Próximos pasos

 [] Automatizar la obtención de datos de tráfico para cualquier ciudad.

 [] Integrar construcción automática de la red con OSMnx.

 [] Publicar resultados como artículo académico.
'''

Autores
Eduardo Guerra – Físico, investigación en redes complejas y dinámica de tráfico.
Chilean Complexity Cluster, Universidad de Chile.

