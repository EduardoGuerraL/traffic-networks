Datos_observacionales = [
"data/processed/DataImages/In_Streets_Coord/Detallado/DataStreetDetR0S1_mean.csv",
"data/processed/DataImages/In_Streets_Coord/Detallado/DataStreetDetR1S1_mean.csv",
"data/processed/DataImages/In_Streets_Coord/Detallado/DataStreetDetR2S3_mean.csv",
"data/processed/DataImages/In_Streets_Coord/Normal/streetsCoordsR0S4.csv",
"data/processed/DataImages/In_Streets_Coord/Normal/streetsCoordsR1S4.csv",
"data/processed/DataImages/In_Streets_Coord/Normal/streetsCoordsR2S4.csv",
"data/processed/DataImages/In_Streets_Coord/Normal/MeanStreetscoordsR0S6.csv"
]

Datos_computacionales = [
"data/processed/DataNetwork/StreetAsNode/all_data_SimpleNet_new.csv",
"data/processed/DataNetwork/StreetAsNode/all_data_ComplexNet_new.csv"
]

# Nuevos archivos de combinaciones (radio x steps)
# Formato: traffic_{mean,max}_N{red}_r{radio}s{steps}.csv
REDES = ["N505", "N1207"]
RADIOS = [0, 1, 2, 3]
STEPS = [3, 6, 10]

def _combinaciones_path(tipo, red, radio, steps):
    """Genera la ruta a un archivo de combinaciones.
    tipo: 'mean' o 'max'
    """
    return f"data/processed/combinaciones/traffic_{tipo}_{red}_r{radio}s{steps}.csv"

# Diccionario para acceso rápido: datos_combinaciones["N505"]["mean"][(0, 3)] -> path
datos_combinaciones = {}
for red in REDES:
    datos_combinaciones[red] = {}
    for tipo in ["mean", "max"]:
        datos_combinaciones[red][tipo] = {}
        for radio in RADIOS:
            for steps in STEPS:
                datos_combinaciones[red][tipo][(radio, steps)] = _combinaciones_path(tipo, red, radio, steps)