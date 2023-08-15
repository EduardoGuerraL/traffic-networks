# FinalVersion
El objetivo es analizar el trafico vehicular de una ciudad y buscar una caracteristica de la red de la ciudad que se acerque al comportamiento de la vida real.

## Screenshot.py

Esto nos sirve para comenzar a obtener imagenes de la ciudad que deseemos. Las capturas son cada 15min.

## NetworkCreator.py

Es una ventana interactiva donde elegimos una imagen de la ciudad y comenzamos a crear los nodos y links de anera manual. 

## getDataFromImages.py

Con esto obtenemos un dataFrame que contiene los valores convertidos de 0 a 255 para los pixels en las coordenadas de los nodos. 

## getDataForNetwork.py

Para obtener los indices de centralidad de la red o el estado asintótico de Ehrenfest. Con el timepo podemos ir calculando nuevos paramentros para incluir en la comparación.

## DataComparator.py

Compara los datos correspondientes a las imagenes (datos observacionales) con los datos que obtenemos de la red (datos computacionales).