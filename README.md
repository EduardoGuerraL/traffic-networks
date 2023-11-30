# Repoitorio se encuentra en proceso de construccion
# Repositorio de Análisis de Tráfico Vehicular

Este repositorio contiene datos y código relacionados con el análisis del tráfico vehicular. A continuación, se describe la estructura de carpetas y el contenido del repositorio.

## Contenido del Repositorio

1. **data**: En esta carpeta se encuentran los datos utilizados en el análisis. Está subdividida en tres subcarpetas:

   - **DataImages**: Contiene datos de imágenes en formato de píxeles para su procesamiento.
   - **DataMakeNetwork**: Aquí se almacenan las redes vehiculares creadas manualmente en */NetworkCreator.py*.
   - **DataNetwork**: Esta subcarpeta contiene datos relacionados con las características de las redes vehiculares creadas a mano.

2. **src**: En esta carpeta se encuentra el código fuente utilizado para analizar el tráfico vehicular. Está subdividida en dos subcarpetas:

   - **Packages**: Contiene paquetes y módulos con funciones y clases específicas para el análisis de tráfico.
   - Archivos `.py`: Estos archivos contienen código que genera gráficos y visualizaciones relacionados con el análisis de tráfico.

3. **.gitignore**: Este archivo especifica qué archivos y carpetas se deben ignorar al realizar seguimiento con Git. Asegura que los archivos generados automáticamente o archivos sensibles no se incluyan en el repositorio.

## Instrucciones de Uso

A continuación, se proporcionan instrucciones básicas para comenzar a trabajar con este repositorio:

1. En *src/Packages/GoogleScreenshot* podemos obtener imagenes del trafico vehicular dando las coordenadas de la ciudad que elegimos. Estas son tomadas cada cuarto de hora por el tiempo que se desee.
2. Con al menos una imagen, podemos crear una red direccionada en *src/Packages/NetworkCreator.py* tomando las intersecciones como nodos y las calles como links. Puede ser tan detallado como se desee. Si se les ocurre otra forma de ver los nodos y links también podria implementarse.
3. Con  *src/Packages/GetDataFromImages.py* podemos convertir las imagenes a matrices de pixeles y linealizando podemos ver cada coordenada como un grado de trafico. Así obtenemos luego un grado de trafico para cada uno de los nodos que cremaos en 2.
4. En *src/Packages/GetDataForNetwork.py* Obtenemos algunas caracteristicas de la red que creamos en 2, además se agregan algunas simulaciones de random walk.
5. En la seccion principal hay varios graficos que estan siendo creados para poder visualizar los datos.
