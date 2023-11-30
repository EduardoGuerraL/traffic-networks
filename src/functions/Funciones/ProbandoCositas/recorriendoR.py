def recorrer_cuadricula(matriz, fila, columna, R):
    for i in range(-R, R+1):
        for j in range(-R, R+1):
            dato = matriz[fila+i][columna+j]
            # Hacer algo con el dato obtenido, por ejemplo, imprimirlo
            print(dato)

# Ejemplo de uso:
# Supongamos una matriz de 5x5 para simplicidad
matriz = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
]
fila_centro = 2
columna_centro = 2
radio = 0

recorrer_cuadricula(matriz, fila_centro, columna_centro, radio)