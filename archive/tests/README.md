# FinalVersion
El objetivo es analizar el trafico vehicular de una ciudad y buscar una caracteristica de la red de la ciudad que se acerque al comportamiento de la vida real.


## Extraction 

Esto es lo que genera los datos que estudiaremos.

### src/extraction/GoogleScreenshot/To_take_screenshot.py

Este programa nos permite obtener una imagen de el trafico vehicular cada cuantos minutos queramos modificando 'period_to_screenshot'. 

Necesitas sacar tu propia clave API de Google Platform.
Poner foto.

### NetworkCreator.py

Es una ventana interactiva donde elegimos una imagen de la ciudad y comenzamos a crear los nodos y links de anera manual. 
Primero necesitas sacar una foto de la ciudad a estudiar, con o sin trafico segun tu referencia. recuerda donde se guarda. La forma de usar es super intuitivo. Solo necesitas importar la imagen despues de haber corrido el programa. 

Especificar más el uso del programa.

## getDataFromImages.py

Con esto obtenemos un dataFrame que contiene los valores convertidos de 0 a 255 para los pixels en las coordenadas de los nodos. 

## getDataForNetwork.py

Para obtener los indices de centralidad de la red o el estado asintótico de Ehrenfest. Con el timepo podemos ir calculando nuevos paramentros para incluir en la comparación.

## DataComparator.py

Compara los datos correspondientes a las imagenes (datos observacionales) con los datos que obtenemos de la red (datos computacionales).