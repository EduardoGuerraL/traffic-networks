import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

def reescalar(data):
    
    max_valor = 255
    min_valor = 0
    
    if min_valor == 0 and max_valor == 0:
        pass
    else:
        data = [round((valor - min_valor) / (max_valor - min_valor),3) for valor in data]

    return data


hora_temp = "08-30"
data_obs_hora = pd.read_csv("data/DataImages/In_Streets_Coord/ForHour_sinFDS/Data_"+str(hora_temp)+".scv")

prom = list(data_obs_hora["Promedio"])
maximo = list(data_obs_hora["Máximo"])
minimo = list(data_obs_hora["Mínimo"])

prom = reescalar(prom)
maximo = reescalar(maximo)
minimo = reescalar(minimo)

X = maximo

#variables independientes
#ehr sim
data_pc = pd.read_csv("datos_comp_percent.csv")
Y = data_pc[data_pc.columns[-1]]


#betweeneess
data_pc = pd.read_csv("datos_network_streets_det.csv")
Z = data_pc["Betweenness_streets"]

#closness
data_pc = pd.read_csv("datos_network_streets_det.csv")
W = data_pc["Closeness_streets"]

# degree
data_pc = pd.read_csv("datos_network_streets_det.csv")
B = data_pc["Degree_streets"]


# X = αY + βW + γZ + \epsilon B
# Datos de ejemplo
X = np.array(X)
Y = np.array(Y)
Z = np.array(Z)
W = np.array(W)

# Ponderación diferencial (basada en los valores de X)
weights = X / np.max(X)

# Construir la matriz de diseño A
A = np.vstack((weights * Y,weights * W, weights * Z, weights * B)).T

# Calcular los coeficientes utilizando el método de los mínimos cuadrados
coefficients, _, _, _ = np.linalg.lstsq(A, X, rcond=None)

# Extraer los coeficientes individuales
alpha = coefficients[0]
beta = coefficients[1]
gamma = coefficients[2]
epsilon = coefficients[3]

print("Coeficiente alpha:", alpha)
print("Coeficiente beta:", beta)
print("Coeficiente gamma:", gamma)
print("Coeficiente epsilon:", epsilon)

#Calcular los valores predichos de X
X_pred = alpha * Y + beta * W + gamma * Z + epsilon * B

# Calcular el error cuadrático medio (ECM)
mse = np.mean((X - X_pred) ** 2)

print("Error cuadrático medio (ECM):", mse)

# Graficar la curva que representa el mínimo
plt.plot(X, label='Valores reales')
plt.plot(X_pred, label='Valores predichos')
plt.xlabel('Índice')
plt.ylabel('X')
plt.legend()
plt.show()
