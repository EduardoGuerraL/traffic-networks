#ifndef VECTOR_H
#define VECTOR_H
#include<iostream>
#include<vector>
#include<cmath>
#include <fstream>

using namespace std;

template <class T>
class Vector
{
private:
    vector<T> A;
public:
    Vector();
    Vector(int, T = T(0)); //Constructor de un vector de largo int lleno de un valor
    Vector(vector<T>); //Vector creado por un vector
    Vector(const Vector<T> &); //Costructor de copia
    ~Vector();
    T & operator[](int);
    T operator[](int) const;
    T & operator()(int);
    T operator()(int) const;
    int Vsize();
    double modulus();
};

template <class T>
Vector<T>::Vector()
{   

}

template <class T>
Vector<T>::Vector(int n, T i)
{
    vector<T> aux(n,i);
    this -> A = aux;
}

template <class T>
Vector<T>::Vector(vector<T> Vec)
{
    this -> A = Vec;
}

template <class T>
Vector<T>::Vector(const Vector<T> & Vec)
{
    this -> A = Vec.A;
}

template <class T>
Vector<T>::~Vector(){}


template <class T>
T & Vector<T>::operator[](int i)
{
    return this -> A[i];
}

template <class T>
T Vector<T>::operator[](int i) const
{
    return this -> A[i];
}

template <class T>
T & Vector<T>::operator()(int i)
{
    return this -> A[i];
}

template <class T>
T Vector<T>::operator()(int i) const
{
    return this -> A[i];
}

template <class T>
int Vector<T>::Vsize(){
    return this -> A.size();
}

template <class T>
double Vector<T>::modulus(){
    double aux;
    for (int i = 0; i < (this -> A.size()); i++ ){
        aux += (this->A[i])*(this->A[i]);
    }
    return sqrt(aux);
}

template <class T>
ostream & operator<<(ostream & os, Vector<T> & a){
    int n = a.Vsize();
    os << "("; 
    for(int i =0; i < (n -1) ; i++ ){
        os << a[i] << ", ";  
    }
    os << a[n-1] << ")";

    return os;
         

}
template <class T>
T punto (Vector<T> a, Vector<T> b){
    T aux=0;
    for(int i = 0; i<(a.Vsize()); i++){
        aux += a[i]*b[i];
    }
    return aux;
}

template <class T>
Vector<T> cruz (Vector<T> a, Vector<T> b){
    vector<T> aux;

    T i,j,k;
    i = a[1] * b[2] - b[1] *a[2];
    j = -(a[0] * b[2] - b[0] *a[2]);
    k = a[0] * b[1] - b[0] *a[1];

    aux.push_back(i);
    aux.push_back(j);
    aux.push_back(k);
    
    return Vector<T>(aux);
}

template <class T>
Vector<T> operator+(Vector<T> a, Vector<T> b){
    vector<T> aux;
    for(int i = 0; i < (a.Vsize()); i++){
        aux.push_back(a[i]+ b[i]);
    }
    return Vector<T>(aux);
}

template <class T>
Vector<T> operator-(Vector<T> a, Vector<T> b){
    vector<T> aux;
    for(int i = 0; i < (a.Vsize()); i++){
        aux.push_back(a[i]- b[i]);
    }
    return Vector<T>(aux);
}

template <class T>
Vector<T> operator*(T a, Vector<T> b){
    vector<T> aux;
    for(int i = 0; i < (b.Vsize()); i++){
        aux.push_back(a * b[i]);
    }
    return Vector<T>(aux);
}

template <class T>
Vector<T> operator*(Vector<T> a, T b){
    vector<T> aux;
    for(int i = 0; i < (a.Vsize()); i++){
        aux.push_back(b * a[i]);
    }
    return Vector<T>(aux);
}

template <class T>
Vector<T> operator*(int a, Vector<T> b){
    vector<T> aux;
    for(int i = 0; i < (b.Vsize()); i++){
        aux.push_back(a * b[i]);
    }
    return Vector<T>(aux);
}

template <class T>
Vector<T> operator*(Vector<T> a, int b){
    vector<T> aux;
    for(int i = 0; i < (a.Vsize()); i++){
        aux.push_back(b * a[i]);
    }
    return Vector<T>(aux);
}

#endif