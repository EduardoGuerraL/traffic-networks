import numpy as np

# Tipos de datos de NumPy con tamaño específico
tipos_de_dato = [
    (np.int8, 'int8'),
    (np.uint8, 'uint8'),
    (np.int16, 'int16'),
    (np.uint16, 'uint16'),
    (np.int32, 'int32'),
    (np.uint32, 'uint32'),
    (np.int64, 'int64'),
    (np.uint64, 'uint64'),
]

# Obtener los valores mínimos y máximos para cada tipo de dato
tabla = []
for tipo, nombre in tipos_de_dato:
    valor_minimo = np.iinfo(tipo).min
    valor_maximo = np.iinfo(tipo).max
    tabla.append((nombre, valor_minimo, valor_maximo))

# Imprimir la tabla
print("| Tipo de dato | Valor mínimo                  | Valor máximo                  |")
print("|--------------|-------------------------------|-------------------------------|")
for nombre, valor_minimo, valor_maximo in tabla:
    print(f"| {nombre:<11} | {valor_minimo:<29} | {valor_maximo:<29} |")