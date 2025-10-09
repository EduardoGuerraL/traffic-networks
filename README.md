# 🚦 Traffic Networks: Análisis de congestión vehicular con teoría de redes complejas

Este proyecto busca **estudiar la congestión vehicular en ciudades a partir de datos de Google Maps y teoría de redes complejas**.  
El caso de estudio inicial es **Punta Arenas (Chile)**, pero la metodología es adaptable a cualquier ciudad.

---

## 📌 Objetivo
Analizar si las métricas de centralidad en redes urbanas (closeness, betweenness, eigenvector, etc.)  
se correlacionan con los niveles reales de congestión vehicular.

---

## 🔹 Flujo de trabajo

1. **Obtención de datos**
   - Imágenes de tráfico vehicular descargadas desde la **API de Google Maps**.
   - Imágenes tomadas cada **15 minutos durante ~2 meses**.
   - Solo se consideran **días de semana** para evitar sesgos de fines de semana.

2. **Procesamiento de imágenes**
   - Cada imagen contiene colores según el tráfico: verde, amarillo, rojo.
   - Se extrae un **promedio de intensidad de tráfico por zona** en cada instante.
   - Se genera una **escala lineal de tráfico** (0 = fluido, 1 = muy congestionado).

3. **Construcción de la red urbana**
   - Inicialmente: creación **manual** de la red a partir de la dirección de calles.
   - En desarrollo: **automatización con OSMnx**.
   - Resultado: grafo dirigido con calles como aristas y esquinas como nodos.

4. **Asignación de tráfico a la red**
   - Cada nodo/arista recibe un valor de tráfico asociado al instante de tiempo correspondiente.

5. **Análisis de redes complejas**
   - Se calculan métricas: closeness, betweenness, eigenvector centrality.
   - Se comparan con los valores de tráfico en el tiempo.

6. **Resultados**
   - Se observan correlaciones más fuertes entre **ciertas métricas de centralidad**  
     y el tráfico vehicular en **horas de alta congestión**.

---

## 📊 Ejemplo de resultados

- Gráficos comparando la evolución temporal de la congestión y las centralidades.
- Mapas urbanos coloreados según el grado de centralidad vs congestión observada.

*(Puedes insertar aquí imágenes de ejemplo de tus plots si quieres que el README brille).*

---

## 🔧 Tecnologías

- **Python 3.12**
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `networkx`, `osmnx` (en desarrollo)
- `opencv` (para procesamiento de imágenes)

---

## 📂 Estructura del repositorio

traffic-networks/
├── src/ # Código fuente organizado
│ ├── data_processing/ # Procesamiento de imágenes y escalas de tráfico
│ ├── network_analysis/ # Construcción y métricas de grafos
│ ├── visualization/ # Gráficos y mapas
│ └── utils/ # Funciones auxiliares
├── notebooks/ # Análisis paso a paso en Jupyter
│ ├── 01_data_exploration.ipynb
│ ├── 02_build_network.ipynb
│ ├── 03_centrality_analysis.ipynb
│ └── 04_results_and_plots.ipynb
├── data/ # (no incluido, solo instrucciones para obtenerlo)
│ └── README.md
├── requirements.txt # Librerías necesarias
└── README.md



---

## 🚀 Cómo usar el proyecto

```bash
# Clonar el repositorio
git clone https://github.com/EduardoGuerraL/CellAuToTraffic
cd traffic-networks

# Instalar dependencias
pip install -r requirements.txt

# Explorar los notebooks
jupyter notebook notebooks/

📌 Próximos pasos

 Automatizar la descarga de imágenes desde Google Maps.

 Integrar construcción automática de la red con OSMnx.

 Publicar resultados como artículo académico.

 ✍️ Autores
Eduardo Guerra – Físico, investigación en redes complejas y dinámica de tráfico.
Chilean Complexity Cluster, Universidad de Chile.

