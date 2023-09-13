from Packages.GetDataForNetwork import NetworkData



if __name__ == "__main__":
    # Probando con ejes
    path_medina = "data/DataMakeNetwork/Medina"
    Medina = NetworkData(path_medina)
    RW = Medina.randomwalkAnalitic_edges()
    df = Medina.getBasicIndexCentralityForEdges()
    df["RW"] = RW
    #Medina.plotEdges(df, "RW", True)

    Matrix_Adj_edges = Medina.getAdjacencyMatrix()[1]
    #print(Matrix_Adj_edges)

print("HOla")