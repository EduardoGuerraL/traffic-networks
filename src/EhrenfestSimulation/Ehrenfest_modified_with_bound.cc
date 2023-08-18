/*
En vez de elegir una particula al azar, elegimos una urna.
*/

#include <iostream>
#include <vector>
#include "./tools/Matriz.h"
#include <fstream>
#include "Functions.h"
#include <stdio.h>
#include <cmath>
#include "./tools/Matriz.h"

using namespace std;

int main()
{
    int particulas = 10000; //Número de paquetes/partículas constantes
    int tiempo = 500000000;  //Número de movimientos/Tiempo
    string archivo_matriz_adjacencia = "data/DataNetwork/StreetAsNode/SimpleNet_adjMatrix.txt";
    string archivo_guardado_estados = "SimpleNet_EhrMod_10mA_500MT_UpperLimit.txt";
    string file_upper_limit_nodes = "data/DataNetwork/StreetAsNode/SimpleNet_max_ocupation_per_streets.txt";

    Matriz<double> Adjacency(archivo_matriz_adjacencia);
    int num_nodos = Adjacency.columnas();

    // Vector de limites:
    ifstream archivo_tope(file_upper_limit_nodes); // Abre el archivo para lectura
    if (!archivo_tope) {
        cerr << "Error al abrir el archivo." << endl;
        return 1;
    }

    vector<int> vector_upper_limit;
    string linea;
    while (getline(archivo_tope, linea)) { // Lee los valores del archivo y los almacena en el vector
        istringstream iss(linea);
        string valor_str;;
        while(getline(iss, valor_str, ',')){
            int valor = stoi(valor_str);
            vector_upper_limit.push_back(valor);
        }
    }
    archivo_tope.close(); // Cierra el archivo

    //Distribuyendo partículas iniciales:
    vector<int> vector_particulas(num_nodos, 0);
    
    // Distribución inicial en una urna:
    //vector_particulas[0] = particulas;

    // Distribución inicial random:
    srand(time(0));
    int contador = particulas;
    while (contador > 0)
    {
        int nodo_inicial = rand() % num_nodos;
        if (vector_particulas[nodo_inicial] < vector_upper_limit[nodo_inicial])
        {
            vector_particulas[nodo_inicial]++;
            contador--;
        }
    }

    // Guardar el estado inicial en un archivo
    ofstream outfile(archivo_guardado_estados);

    // Main: Moviendo las partículas
    srand(time(0));
    for (int t = 0; t < tiempo; t++)
    {
        // Escoger un nodo al azar
        int nodo_origen = rand() % num_nodos;

        int particulas_nodo_origen = vector_particulas[nodo_origen];
        if (particulas_nodo_origen > 0)
        {

            vector<int> nodos_destino;
            for (int i = 0; i < Adjacency.filas(); i++)
            {
                if (Adjacency(nodo_origen, i) == 1)
                {
                    nodos_destino.push_back(i);
                }
            }

            if (!nodos_destino.empty())
            {
                int nodo_destino = nodos_destino[rand() % nodos_destino.size()];
                if (vector_particulas[nodo_destino] < vector_upper_limit[nodo_destino])
                {
                    vector_particulas[nodo_origen]--;
                    vector_particulas[nodo_destino]++;

                    // Guardar el estado actual en el archivo
                    if (t % particulas == 0){
                        outfile << vector_particulas << endl;
                    }
                }
            }
        }
    }
    cout << vector_particulas << endl;
    return 0;
}
