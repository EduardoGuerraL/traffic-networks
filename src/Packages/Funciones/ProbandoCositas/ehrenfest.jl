using Random

function simular_iteraciones(matriz_adyacencia, vector_tope, dataFrameLessOne = nothing, cantidad_particulas = 6, iteraciones = 100)
    # Obtenemos la cantidad de nodos
    num_nodos = length(matriz_adyacencia)

    if dataFrameLessOne === nothing
        # Creamos un vector para almacenar la cantidad de partículas en cada nodo
        vector_particulas = zeros(Int, num_nodos)
        println(vector_particulas)
        # Distribuimos las partículas inicialmente de manera uniforme en los nodos
        contador = cantidad_particulas
        while contador > 0
            nodo_inicial = rand(1:num_nodos)
            if vector_particulas[nodo_inicial] < vector_tope[nodo_inicial]
                vector_particulas[nodo_inicial] += 1
                contador -= 1
            end
        end
    elseif dataFrameLessOne !== nothing
        vector_particulas = dataFrameLessOne[:, end]
    else
        println("No se entregó la instrucción correcta al dar un archivo de la iteración anterior")
        return
    end

    # Realizamos las iteraciones
    for _ in 1:iteraciones
        # Elegimos una partícula al azar
        nodo_origen = rand(1:num_nodos)
        particulas_origen = vector_particulas[nodo_origen]

        # Si hay partículas en el nodo de origen
        if particulas_origen > 0
            # Elegimos un nodo destino aleatoriamente
            nodos_destino = findall(x -> x == 1, matriz_adyacencia[nodo_origen, :])
            if length(nodos_destino) > 0
                nodo_destino = rand(nodos_destino)
                # Si el destino no está lleno
                if vector_tope[nodo_destino] > vector_particulas[nodo_destino]
                    # Movemos una partícula del nodo origen al nodo destino
                    vector_particulas[nodo_origen] -= 1
                    vector_particulas[nodo_destino] += 1
                end
            end
        end
    end

    return vector_particulas
end

matriz_adyacencia = [   0 1 1 0   
                        1 0 1 1   
                        1 1 0 1
                        0 1 1 0
                    ]

vector_tope = [3, 3, 3, 1]

resultado_simulacion = simular_iteraciones(matriz_adyacencia, vector_tope)
println("Resultado de la simulación: ", vector_tope)
