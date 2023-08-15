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
    string archivo_matriz_adjacencia = "matriz_simple_ejes.txt";
    string archivo_guardado_estados = "Ehrenfest_estado_500Miter_10mautos_matrixSimple.txt";

    Matriz<double> Adjacency(archivo_matriz_adjacencia);
    int num_nodos = Adjacency.columnas();

    //Distribuyendo partículas iniciales:
    vector<int> vector_particulas(num_nodos, 0);
    //vector_particulas[0] = particulas;

    srand(time(0));

    int contador = particulas;
    while (contador > 0)
    {
        int nodo_inicial = rand() % num_nodos;
        vector_particulas[nodo_inicial]++;
        contador--;

    }

    // Imprimir el resultado
    cout << "Estado inicial:" << endl;
    for (int i = 0; i < 5; i++)
    {
        cout << "Nodo " << i << ": " << vector_particulas[i] << " partículas" << endl;
    }
    cout << "..." << endl;

    // Guardar el estado inicial en un archivo
    ofstream outfile(archivo_guardado_estados);
    if (outfile.is_open())
    {
        
        cout << "Archivo abierto" << endl;
        
    }
    else
    {
        cerr << "No se pudo abrir el archivo para escribir." << endl;
        return 1;
    }

    srand(time(0));
    for (int t = 0; t < tiempo; t++)
    {
        // Escoger una partícula al azar
        int particula_aleatoria = rand() % particulas;
        int nodo_origen = -1;

        // Encontrar el nodo actual de la partícula seleccionada
        int contador_particulas = 0;
        for (int nodo = 0; nodo < num_nodos; nodo++)
        {
            if (vector_particulas[nodo] > 0)
            {
                contador_particulas += vector_particulas[nodo];
                if (contador_particulas > particula_aleatoria)
                {
                    nodo_origen = nodo;
                    break;
                }
            }
        }

        if (nodo_origen != -1)
        {
            int particula_origen = vector_particulas[nodo_origen];

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
                
                vector_particulas[nodo_origen]--;
                vector_particulas[nodo_destino]++;
                
                // Guardar el estado actual en el archivo
                if (t % particulas == 0){
                    outfile << vector_particulas << endl;
                }
                
                
            }
        }
    }
    cout << vector_particulas << endl;
    return 0;
}
