import pandas as pd

def quitar_sabado_domingo(df):
    # Convierte las columnas de fecha a tipo datetime
    fechas = pd.to_datetime(df.columns[2:-1], format="/%Y-%m-%d_%H-%M")
    
    # Obtiene el índice de las columnas que corresponden a los sábados y domingos
    columnas_sabado_domingo = df.columns[2:-1][(fechas.weekday == 5) | (fechas.weekday == 6)]
    
    # Elimina las columnas correspondientes a los sábados y domingos
    df_filtrado = df.drop(columnas_sabado_domingo, axis=1)
    
    return df_filtrado

import pandas as pd

def obtener_promedio_maximo_por_hora(df_filtrado):
    columnas = df_filtrado.columns[5:-1]
    horas = [col.split("_")[1].split(".")[0] for col in columnas]
    horas_unicas = set(horas)
    dfs_hora = []

    for hora in horas_unicas:
        columnas_hora = [col for col in columnas if col.endswith(f"_{hora}.png")]
        df_hora = df_filtrado[columnas_hora].copy()

        df_hora['Promedio'] = df_hora[columnas_hora].mean(axis=1)
        df_hora['Máximo'] = df_hora[columnas_hora].max(axis=1)
        df_hora['Mínimo'] = df_hora[columnas_hora].min(axis=1)

        df_hora.to_csv("data/DataImages/In_Streets_Coord/ForHour_sinFDS/Data_"+str(hora)+".scv")

    return dfs_hora


df = pd.read_csv("data/DataImages/In_Intersection_Coord/Detallado/intersectionCoord_detallado.csv")

df_filtrado =  quitar_sabado_domingo(df)

df_filtrado.to_csv("data/DataImages/In_Intersection_Coord/Detallado/intersectionCoord_sinFDS_detallado.csv")

print(df_filtrado)
