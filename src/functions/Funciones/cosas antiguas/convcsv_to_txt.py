import csv

# Ruta del archivo CSV de entrada y salida
archivo_entrada = 'data/DataNetwork/StreetAsNode/ComplexNet_Max_ocupation_per_strets.csv'
archivo_salida = 'ComplexNet_max_ocupation_per_streets.txt'

# Leer valores de la segunda columna del archivo CSV
valores_segunda_columna = []
with open(archivo_entrada, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Saltar el encabezado si existe
    for row in reader:
        valor = int(row[1])
        valores_segunda_columna.append(valor)

# Convertir los valores en una cadena separada por comas
cadena_valores = ','.join(str(valor) for valor in valores_segunda_columna)

# Escribir la cadena de valores en el archivo de salida
with open(archivo_salida, 'w') as txtfile:
    txtfile.write(cadena_valores)

