import pandas as pd

def agregar_columna(df_base, columna_a_agregar, nombre_nueva_columna):
    """
    Agrega una columna a un DataFrame y devuelve el DataFrame resultante.
    
    Args:
        df_base (pd.DataFrame): DataFrame al que se agregará la columna.
        columna_a_agregar (pd.Series): Columna que se agregará al DataFrame.
        nombre_nueva_columna (str): Nombre para la columna que se agregará.
        
    Returns:
        pd.DataFrame: DataFrame resultante con la columna agregada.
    """
    df_result = pd.concat([df_base, columna_a_agregar], axis=1)
    df_result[nombre_nueva_columna] = columna_a_agregar
    df_result = df_result.drop(columna_a_agregar.name, axis=1)
    return df_result

#Unificando datos Complex
"""
cx = "data/DataNetwork/StreetAsNode/ResultData/ComplexNet_Ehr_10mA_500MT.csv"
cx_lim = "data/DataNetwork/StreetAsNode/ResultData/ComplexNet_Ehr_10mA_500MT_UpperLimit.csv"

cx_mod = "data/DataNetwork/StreetAsNode/ResultData/ComplexNet_EhrMod_10mA_500MT.csv"
cx_mod_lim = "data/DataNetwork/StreetAsNode/ResultData/ComplexNet_EhrMod_10mA_500MT_UpperLimit.csv"

cx_centrality = "data/DataNetwork/StreetAsNode/ResultData/ComplexNet_IndicesCentralidad.csv"

cx_max_ocupation = "data/DataNetwork/StreetAsNode/ResultData/ComplexNet_max_ocupation_per_streets.csv"

cx_alldata = "data/DataNetwork/StreetAsNode/All_data_ComplexNet.csv"
datacx_alldata = pd.read_csv(cx_alldata)

datacx = pd.read_csv(cx)
datacx_lim = pd.read_csv(cx_lim)
datacx_mod = pd.read_csv(cx_mod)
datacx_mod_lim = pd.read_csv(cx_mod_lim)

df_mean = datacx.mean(axis=1)
datacx_alldata["mean_state_RW"] = df_mean
df_mean = datacx_lim.mean(axis=1)
datacx_alldata["mean_state_RW_lim"] = df_mean
df_mean = datacx_mod.mean(axis=1)
datacx_alldata["mean_state_RWM"] = df_mean
df_mean = datacx_mod_lim.mean(axis=1)
datacx_alldata["mean_state_RWM_lim"] = df_mean

datacx_alldata.to_csv("all_data_ComplexNet_new.csv")


"""
"""
datacx_centrality = pd.read_csv(cx_centrality)
datacx_max_ocupation = pd.read_csv(cx_max_ocupation)
"""




"""
new = agregar_columna(datacx_centrality, datacx[datacx.columns[-1]], "state RW")
new = agregar_columna(new, datacx_lim[datacx_lim.columns[-1]], "state_RW_UL")
new = agregar_columna(new, datacx_mod[datacx_mod.columns[-1]], "state_RWM")
print(datacx_centrality.info())
new = agregar_columna(new, datacx_mod_lim[datacx_mod_lim.columns[-1]], "state_RWM_UL")
new = agregar_columna(new, datacx_max_ocupation[datacx_max_ocupation.columns[-1]], "MaxOcupation")
print(new.info())

new.to_csv("data/DataNetwork/StreetAsNode/ResultData/All_data_ComplexNet.csv")

"""
#Unificando datos Simple


sp = "data/DataNetwork/StreetAsNode/ResultData/SimpleNet_Ehr_10mA_500MT.csv"
sp_lim = "data/DataNetwork/StreetAsNode/ResultData/SimpleNet_Ehr_10mA_500MT_UpperLimit.csv"

sp_mod = "data/DataNetwork/StreetAsNode/ResultData/SimpleNet_EhrMod_10mA_500MT.csv"
sp_mod_lim = "data/DataNetwork/StreetAsNode/ResultData/SimpleNet_EhrMod_10mA_500MT_UpperLimit.csv"

sp_centrality = "data/DataNetwork/StreetAsNode/ResultData/SimpleNet_IndicesCentralidad.csv"

sp_max_ocupation = "data/DataNetwork/StreetAsNode/ResultData/SimpleNet_max_ocupation_per_streets.csv"

datasp = pd.read_csv(sp)
datasp_lim = pd.read_csv(sp_lim)
datasp_mod = pd.read_csv(sp_mod)
datasp_mod_lim = pd.read_csv(sp_mod_lim)
datasp_centrality = pd.read_csv(sp_centrality)
datasp_max_ocupation = pd.read_csv(sp_max_ocupation)

sp_alldata = "data/DataNetwork/StreetAsNode/All_data_ComplexNet.csv"
datasp_alldata = pd.read_csv(sp_alldata)

df_mean = datasp.mean(axis=1)
datasp_alldata["mean_state_RW"] = df_mean
df_mean = datasp_lim.mean(axis=1)
datasp_alldata["mean_state_RW_lim"] = df_mean
df_mean = datasp_mod.mean(axis=1)
datasp_alldata["mean_state_RWM"] = df_mean
df_mean = datasp_mod_lim.mean(axis=1)
datasp_alldata["mean_state_RWM_lim"] = df_mean

datasp_alldata.to_csv("all_data_SimpleNet_new.csv")
"""
print(datasp_centrality.info())
new1 = agregar_columna(datasp_centrality, datasp[datasp.columns[-1]], "state RW")
new1= agregar_columna(new, datasp_lim[datasp_lim.columns[-1]], "state_RW_UL")
new1 = agregar_columna(new, datasp_mod[datasp_mod.columns[-1]], "state_RWM")
new1 = agregar_columna(new, datasp_mod_lim[datasp_mod_lim.columns[-1]], "state_RWM_UL")
new1 = agregar_columna(new, datasp_max_ocupation[datasp_max_ocupation.columns[-1]], "MaxOcupation")
print(new1.info())

new1.to_csv("data/DataNetwork/StreetAsNode/ResultData/All_data_SimpleNet.csv")

"""