#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include <iostream>
#include <vector>
#include <fstream>
#include "./tools/Matriz.h"

using namespace std;


vector<int> ContarUnos(Matriz<int> A)
{
    vector<int> Aux;
    for (int i = 0; i < int(A.columnas()); i++)
    {
        int contador = 0;
        for(int j = 0; j < int(A.filas()); j++)
        {
            if(A(j,i) == 1)
            {
                contador ++;
            }
        }
        Aux.push_back(contador);
    }
    return Aux;
}

/*
//Esta probabilidad va a ser segun el paper.
double Probabilidad(int inicio, int final, double g)
{
    double T;


    T = 1 / (exp(-g/(N*(n_i - n_j - 1))) + 1);

    return T;
} 
*/

void Makedats(int NP, Vector<double> eig_vec, Matriz<int> Cantidad)
{
       //Creando pdf

    fstream tex;
    tex.open("script.gp", ios::out);
    tex << "set encoding utf8" << endl;
    tex << endl;
    tex << "set terminal pdf" << endl;
    tex << "set output \"grafico.pdf\"" << endl;
    tex << endl;
    tex << "set xlabel \"Tiempo\"" << endl;
    tex << "set ylabel \"Particulas\"" << endl;
    for (int i = 0; i < int(eig_vec.Vsize()); i++)
    {
        tex << "set arrow from " << 0 <<","<< eig_vec[i] << " to " << NP <<","<< eig_vec[i] << " nohead ls " << i+1 <<" lw 0.5 " << endl;
    }
    
    tex << "plot \"datos.dat\" u 1:2 w l title \"Urna 0\"";
    for (int i = 0; i < int(Cantidad.columnas()) - 1; i++)
    {
        tex << ", \"datos.dat\" u 1:" << i+3 <<" w l title \"Urna " << i+1 << "\"";  
    }
    tex << endl;
    tex.close();
    

    //CREAR UN SCRIPT QUE GRAFIQUE ESTO SIN IMPORTAR EL TAMAÑO DE URNAS
    fstream archivo;
    archivo.open("datos.dat", ios::out);

    for(int i = 0; i < Cantidad.filas() ; i++)
    {
        archivo << i << "\t";
        for(int j = 0; j < Cantidad.columnas(); j++)
        {
            archivo << Cantidad(i,j) << "\t";
        }
        archivo << endl;
    }
    archivo.close();
}


#endif