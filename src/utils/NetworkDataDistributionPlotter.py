"""
Nos muestra un grafico con las distribuciones de los valores de centralidad y otros de la red.
"""

import pandas as pd
from functions.basics import plot_distribution

#Simple 

data = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv")
print(data.info())

BC = data["BC"]
CC = data["CC"]
DC = data["DC"]
DiBC = data["DiBC"]
DiCC = data["DiCC"]
DiDC = data["DiDC"]
Max_ocupation = data["MaxOcupation"]
mean_rw = data["mean_state_RW"]
mean_rwm = data["mean_state_RWM"]
mean_rw_uplim = data["mean_state_RW_lim"]
mean_rwm_uplim = data["mean_state_RW_lim"]

#Complejo

data = pd.read_csv("data/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv")
print(data.info())

plot_distribution(BC, "C_B")
plot_distribution(CC, "C_C")
plot_distribution(DC, "C_D")
plot_distribution(DiBC, "C_{DB}")
plot_distribution(DiCC, "C_{DC}")
plot_distribution(DiDC, "C_{DD}")
plot_distribution(mean_rw, r"\langle N \rangle_{rw}")
plot_distribution(mean_rwm, r"\langle N \rangle_{rwm}")
plot_distribution(mean_rw_uplim, r"\langle N \rangle_{rw(lim)}")
plot_distribution(mean_rwm_uplim, r"\langle N \rangle_{rwm(lim)}")
plot_distribution(Max_ocupation, "N_{max}")