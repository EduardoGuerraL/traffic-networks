#ifndef MATRIZ_H
#define MATRIZ_H

#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <string>
#include <sstream>
#include "Vector.h"

using namespace std;



template <class T>
class Matriz
{
private:
    vector<vector<T>> matrix;

public:
    //------------CONSTRUCTORES-----------------------------------------------------------
    Matriz();                       //Dice que existe una matriz            (Matriz<double> A;)
    Matriz(vector<vector<T>>);      //Crea matriz con vector de vectores    (Matriz<double> A(a);, a un vector<vector<>>;)
    Matriz(int,int);                //Crea matriz(n x m) de puros 0s.       (Matriz<T> A(3,3);)
    Matriz(int, int, T);            //Crea matriz(n x m) de valor dado T.   (Matriz<T> A(3,3,1);)
    Matriz(const Matriz<T> &);
    Matriz(string);          
    Matriz(int);                    //Crea matriz identidad cuadrada.       (Matriz<T> A(3);)
    ~Matriz();


//---------------OPERADORES------------------------------------------------------------

    Matriz<T> operator=(const Matriz<T> &);
    T operator()(int, int) const;   //MOSTRAR ELEMENTO I,J
    T & operator()(int, int);
  //Matriz<T> operator+(const Matriz<T> &, const Matriz<T> &);      //Suma de matrices
  //Matriz<T> operator-(const Matriz<T> &, const Matriz<T> &);      //Resta de matrices
  //Matriz<T> operator*(const Matriz<T> &, const Matriz<T> &);      //Multiplicación de matrices
  //vector<T> operator * (Matrices<T> , vector<T> )


    //-------------FUNCIONES--------------------------------------------------------------

    vector<vector<T>> get();        //MOSTRAR ELEMENTOS
    int filas();                    //CANTIDAD DE FILAS
    int columnas();                 //CANTIDAD DE COLUMNAS
    void set_fila(int, vector<T>);
    void set_columna(int, vector<T>);
    vector<T> get_fila(int);
    vector<T> get_columna(int);
    void switch_filas(int, int);
    void switch_columnas(int, int);
    Matriz<T> get_diagonal(int, T);
    Matriz<T> get_diagonal(vector<T>);
    Matriz<T> get_tridiagonal(vector<T>, vector<T>, vector<T>);
    Matriz<T> get_tridiagonal(int, T, T, T);
    void resize(int /*fila*/, int);
    void equalsize(Matriz<T> &);
    Matriz<T> inversa(const Matriz<T> &);
    Matriz<T> tringular_superior(const Matriz<T> &);
    Matriz<T> transpuesta(); 
    vector<Matriz<T>> LU();
    T mult_diag();
    void mult_fila();
    double LeviCita(int, int,int);
};



//################################################################################################
//################-------CONSTRUCTORES---------###################################################
//################################################################################################



template <class T>
Matriz<T>::Matriz(){}


template <class T>
Matriz<T>::Matriz(vector<vector<T>> A)
{
    this -> matrix = A;
}


template <class T>
Matriz<T>::Matriz(int n, int m)
{
    vector<vector<T>> M;
    vector<T> vectores;
    for(int i = 0; i < m ; i++){
        vectores.push_back(0);
    }
    for (int j = 0; j< n; j++){
        M.push_back(vectores);
    }
    matrix = M;
}


template <class T>
Matriz<T>::Matriz(int n, int m, T a)
{
    vector<vector<T>> M;
    vector<T> vectores;
    for(int i = 0; i < m ; i++){
        vectores.push_back(a);
    }
    for (int j = 0; j< n; j++){
        M.push_back(vectores);
    }
    matrix = M;
}


template <class T>
Matriz<T>::Matriz(const Matriz & A)
{
    this -> matrix = A.matrix;
}


template <class T>
Matriz<T> Matriz<T>::operator=(const Matriz<T> & X){
    if(this!=&X)
    {
      this->matrix = X.matrix;
    }
  
  return *this;
}


template <class T>
Matriz<T>::Matriz(int n)
{
    vector< vector<T> > aux;
    for(int i = 0; i < n; i++)
    {
        vector<T> aux1(n,T(0));
        aux1[i] = T(1);
        aux.push_back(aux1);
    }

    matrix = aux;

}


template <class T>
Matriz<T>::Matriz(string Archivo)
{
   string filename = Archivo;
   vector<vector<double> > data;
   ifstream in( filename );
   for ( string line; getline( in, line ); )
   {
      stringstream ss( line );
      vector<double> row;
      for ( string d; ss >> d; )
      {
          row.push_back( stod(d) );
      } 
      data.push_back( row );
   }

    matrix = data;
}


template <class T>
Matriz<T>::~Matriz(){}



//#################################################################################################
//##############-------FUNCIONES------#############################################################
//#################################################################################################



//OBTENER VECTOR DE VECTORES A PARTIR DE LA MATRIZ
template <class T>
vector<vector<T>> Matriz<T>::get(){
    return matrix;
}

//NUMERO DE FILAS
template <class T>
int Matriz<T>::filas(){
    return matrix.size();
}

//NUMERO DE COLUMNAS
template <class T>
int Matriz<T>::columnas(){
    return int(matrix[0].size());
}
    
//CAMBIAR TAMAÑO DE n x m  A UNA MATRIZ DE a x b. RELLENANDO EL RESTO CON CEROS.
template <class T>
void Matriz<T>::resize(int a, int b){
    if(a > (int)this->matrix.size() && b > (int)this->matrix[0].size())
    {
        //Resize para columnas
        for(int i = 0; i < (int)this->matrix.size(); i++)
        {
            for(int j = this->matrix.size(); j < b; j++)
            this->matrix[i].push_back(0);
        }
        //Resize para filas
        vector<T> temp;
        for(int i = 0; i < (int)matrix[0].size(); i++){
            temp.push_back(0);
        }
        for(int i = (int)this->matrix.size(); i < a; i++)
        {
            matrix.push_back(temp);
        }
    }
    else if(a <= (int)this->matrix.size())
    {
        //Resize para columnas
        for(int i = 0; i < (int)this->matrix.size(); i++)
        {
            for(int j = this->matrix.size(); j < b; j++)
            this->matrix[i].push_back(0);
        }
    }
    else if(b <= (int)this->matrix[0].size())
    {
        //Resize para filas
        vector<T> temp;
        for(int i = 0; i < (int)matrix[0].size(); i++){
            temp.push_back(0);
        }
        for(int i = (int)this->matrix.size(); i < a; i++)
        {
            matrix.push_back(temp);
        }
    }
 
}

//INGRESAR VECTOR COMO FILA DE MATRIZ:
template<class T>
void Matriz<T>::set_fila(int j, vector <T> A){
    int n = A.size();
    for (int i = 0; i < n; i++)
    {
        matrix[j][i] = A[i];
    }
}

//INGRESAR VECTOR COMO COLUMNA:
template<class T>
void Matriz<T>::set_columna(int j, vector <T> A){
    int n = A.size();
    for (int i = 0; i < n; i++)
    {
        matrix[i][j] = A[i];
    }
}

//OBTENER LA FILA i-ESIMA: 
template<class T>
vector<T> Matriz<T>::get_fila(int i){
    int n = matrix.size();
    vector<T> aux(n);
    for (int j = 0; j < n; j++)
    {
        aux[j] = matrix[i][j];
    }
    return aux;
}

//OBTENER LA COLUMNA i-ESIMA:
template<class T>
vector<T> Matriz<T>::get_columna(int j){
    int n = matrix[0].size();
    vector<T> aux(n);
    for (int i = 0; i < n; i++)
    {
        aux[i] = matrix[i][j];
    }
    return aux;
}

template<class T>
void Matriz<T>::switch_filas(int n1,int n2){

    int nfilas = matrix.size();
    int ncolumnas = matrix[0].size();

    Matriz<T> A(matrix);

    vector<T> fila1 = A.get_fila(n1);
    vector<T> fila2 = A.get_fila(n2);

    A.set_fila(n1,fila2);
    A.set_fila(n2,fila1);

    for(int i=0;i<nfilas;i++){
        for(int j=0;j<ncolumnas;j++){
            matrix[i][j] = A(i,j);
        }
    }
}

template<class T>
void Matriz<T>::switch_columnas(int n1,int n2){

    int nfilas = matrix.size();
    int ncolumnas = matrix[0].size();

    Matriz<T> A(matrix);

    vector<T> columna1 = A.get_columna(n1);
    vector<T> columna2 = A.get_columna(n2);

    A.set_columna(n1, columna2);
    A.set_columna(n2, columna1);

    for(int i=0;i<nfilas;i++){
        for(int j=0;j<ncolumnas;j++){
            matrix[i][j] = A(i,j);
        }
    }
}


//Retorna una matriz diagonal con los valores dados
template <class T>
Matriz<T> get_diagonal(vector<T> B){

  int dim = B.size();
  Matriz<T> A(dim);

  for(int i=0;i<dim;i++){
    for(int j=0;j<dim;j++){
      A(i,i) = B[i];
        if(j != i){
	        A(i,j) = 0*B[i];
        } 
    }
  }
  return A;
}

template <class T>
Matriz<T> get_diagonal(int dim, T b){

  Matriz<T> A(dim);

  for(int i=0;i<dim;i++){
    for(int j=0;j<dim;j++){
      A(i,i) = b;
        if(j != i){
	        A(i,j) = 0*b;
        } 
    }
  }
  return A;
}

//Retorna una matriz tridiagonal con los valores dados
template <class T>
Matriz<T> get_tridiagonal(vector<T> diag, vector<T> Lowerdiag, vector<T> Upperdiag){

int dim = diag.size();

Matriz<T> D = get_diagonal(diag);
Matriz<T> L(dim,dim,0*Lowerdiag[0]);
Matriz<T> U(dim,dim,0*Lowerdiag[0]);

for(int i=0;i<dim-1;i++){
	U(i,i+1) =  Upperdiag[i];
}
for(int i=0;i<dim-1;i++){
	L(i+1,i) =  Lowerdiag[i];
}
return D + L + U;
}

template <class T>
Matriz<T> get_tridiagonal(int dim, T b_diag, T b_Lowerdiag, T  b_Upperdiag){

Matriz<T> D = get_diagonal(dim, b_diag);
Matriz<T> L(dim,dim,0*b_Lowerdiag);
Matriz<T> U(dim,dim,0*b_Lowerdiag);

for(int i=0;i<dim-1;i++){
	U(i,i+1) =  b_Upperdiag;
}
for(int i=0;i<dim-1;i++){
	L(i+1,i) =  b_Lowerdiag;
}
return D + L + U;
}



//INVERSA DE UNA MATRIZ
template <class T>
Matriz<T> inversa( Matriz<T> & A){

    int n = A.filas();

    Matriz<T> I(n);

    Matriz<T> C = A;
    
    for(int k = 0; k < C.filas(); k++){
        double temp = C(k,k);
        for(int i = k; i < C.columnas(); i++)
        {
            C(k,i) = C(k,i)/temp;
            I(k,i) = C(k,i)/temp;

        }
        for(int j = k+1; j<C.filas(); j++)
        {
            double piv = C(j,k);
            for(int i = k; i < C.columnas(); i++)
            {
                C(j,i) = C(j,i) - C(k,i)*piv;
                I(j,i) = C(j,i) - C(k,i)*piv;
            }
        }
    }

    Matriz<T> aux = C.transpuesta();
    Matriz<T> auxI = I.transpuesta();

    for(int k = 0; k < C.filas(); k++){
        double temp = aux(k,k);
        for(int i = k; i < C.columnas(); i++)
        {
            aux(k,i) = aux(k,i)/temp;
            auxI(k,i) = aux(k,i)/temp;

        }
        for(int j = k+1; j<C.filas(); j++)
        {
            double piv = aux(j,k);
            for(int i = k; i < C.columnas(); i++)
            {
                aux(j,i) = aux(j,i) - aux(k,i)*piv;
                auxI(j,i) = aux(j,i) - aux(k,i)*piv;
            }
        }
    }
    
    return auxI;
}

template <class T>
 Matriz<T> tringular_superior(Matriz<T> & A){

     Matriz<T> C = A;
     for(int k = 0; k < C.filas(); k++){
        double temp = C(k,k);
        for(int i = k; i < C.columnas(); i++){
            C(k,i) = C(k,i)/temp;
        }
        for(int j = k+1; j<C.filas(); j++){
            double piv = C(j,k);
            for(int i = k; i < C.columnas(); i++){
                C(j,i) = C(j,i) - C(k,i)*piv;
            }
        }
    }
    return C;
}

//Transpuesta de una matriz
template <class T>
Matriz<T> Matriz<T>::transpuesta()
{
    Matriz<T> aux(matrix);
    vector<T> aux1 (aux.filas());
    vector<vector<T>> matriz1(aux.columnas(), aux1);
    Matriz<T> matriz(matriz1);
    for(int i = 0; i < matriz.filas(); ++i)
    {
        for(int j = 0; j < matriz.columnas(); ++j)
        {
            matriz(i,j) = aux(j,i);
        }
    }
    return matriz;
}

//Le das una matriz y la descompone en LU
template<class T>
vector<Matriz<T>> Matriz<T>::LU()
{
    int n = matrix.size();
    Matriz<T> L(n,n);
    Matriz<T> U(n,n);

    for(int i = 0; i < n; i++)
    {
        //producto entre L y U
        for(int k = 0; k < n; k++)
        {
            T suma = 0;
            for(int j = 0; j<n; j++)
            {
                suma += L(i,j)*U(j,k);
            }
            U(i,k) = matrix[i][k] - suma;
        }
        for(int k=0; k < n; k++)
        {
            if(i==k)
            {
                L(i,i) = T(1);
            }
            else
            {
                T suma = 0;
                for(int j = 0; j<n; j++)
                {
                    suma += L(k,j)*U(j,i);
                }
                L(k,i) = (matrix[k][i]-suma)/ U(i,i);
            }
            
        }
    }
    vector<Matriz<T>> Aux;
    Aux.push_back(L);
    Aux.push_back(U);

    return Aux;

}


//Multiplicación de la diagonal
template<class T>
T Matriz<T>::mult_diag()
{
    T mult = 1;
    Matriz<T> aux= matrix;
    int n = aux.filas();
    for(int i = 0; i < n; i++)
    {
        mult *= aux(i,i);
    }
    return mult;
}

//Se implementa la funcion LeviCita emulando al pseudotensor LeviCita
//--------------------------
double LeviCita(int i, int j,int k){
  if((i==0)&&(j==1)&&(k==2)){
    return 1.0;
  }
  else if((i==2)&&(j==0)&&(k==1)){
    return 1.0;
  }
  else if((i==1)&&(j==2)&&(k==0)){
    return 1.0;
  }
  else if((i==j)||(j==k)||(k==i)){
    return 0;
  }
  else{
    return -1.0;
  }
}


//Se implementa la funcion que resuelve un sistema de ecuaciones lineal con una matriz triangular inferior sin ceros en su diagonal a traves de una substitucion hacia atras
//---------------------- 
template <class T>
vector<T> LowerBackSubstitution(Matriz<T> A, vector<T> b){

    int n = b.size();
    vector<T> x(n);
    x[0] = b[0]/A(0,0);

    T sumatoria = 0;
    for(int i=1;i<n;i++){
        for(int j=0;j<i;j++){
            sumatoria+= A(i,j)*x[j];
        }
    x[i] = (b[i]-sumatoria)/A(i,i);
    sumatoria = 0;
    }
    return x;
}

//Se implementa la funcion que devuelve la inversa de una matriz triangular inferior sin ceros en su diagonal
//----------------------------
template <class T>
Matriz<T> InversaTriangularInferior(Matriz<T> L){

    int n = L.columnas();
    Matriz<T> I(n);
    Matriz<T> Linversa(n);
    vector<T> x(n);

    vector<T> b(n);
    for(int i=0;i<n;i++){
        b = I.get_fila(i);
        x = LowerBackSubstitution(L,b);
        Linversa.set_columna(i,x);
    }
return Linversa;
}

//Se implementa una funcion que devuelve la inversa de la diagonal de una matriz
//-----------------------------
template<class T>
Matriz<T> InversaDiagonal(Matriz<T> D){
    int n = D.filas();
    Matriz<T> InversaD(n,n,0);
    for(int i=0;i<n;i++){
            InversaD(i,i) = 1.0/D(i,i);
        }
return InversaD;
}

//Se implementa una funcion que transforma un objeto Matrices< Matrices<T> > en un objeto Matrices<T>, es decir transforma una matriz con bloques de matrices de igual tamanio en una matriz normal 
//-------------------------------
template <class T>
Matriz<T> Unblock(Matriz<Matriz<T>> H){

    int dimf_h = H.filas();
    int dimc_h = H.columnas();

    int n = H(0,0).filas();
    int m = H(0,0).columnas();

    int dimf = n*dimf_h;
    int dimc = m*dimc_h;

    Matriz<T> A(dimf,dimc);

    int f = 0;
    for(int ih=0;ih<dimf_h;ih++){
        for(int jh=0;jh<dimc_h;jh++){
            for(int ik=0;ik<n;ik++){
                for(int jk=0;jk<m;jk++){
                    A(ik +n*ih,jk + m*jh) = (H(ih,jh))(ik,jk); 
                }
            }
        }
    }
    return A;
}



//Se obtiene el determinante usando la descomposicion de Crout, A = LU  => det(A) = det(L)det(U)
//(El algoritmo falla si A.get(0,0) == 0) 
//---------------------------------
template<class T> 
T DeterminantCroutDescomposition(Matriz<T> A){

    int dim = A.filas();

    Matriz<T> L = A.LU()[0];
    Matriz<T> U = A.LU()[1];

    T det_L = 1;
    T det_U = 1;

    for(int i=0;i<dim;i++){
        det_L = det_L*L(i,i);
        det_U = det_U*U(i,i);
    }
    return det_L*det_U;
}

//Resolucion de un sistema lineal con matriz tridiagonal usando el algoritmo de Thomas, 
//donde "b" es la diagonal, "a" es la diagonal inferior, "c" es la diagonal superior y "d" es el resultado de la matriz por el vector solucion.
//------------------------------
template<class T>
vector<T> TridiagonalThomasAlgorithm(vector<T> a, vector<T> b, vector<T> c, vector<T> d){

    int dim = b.size(); 

    vector<T> x(dim);

    vector<T> C_(dim-1);
    vector<T> B_(dim);
    vector<T> D_(dim);

    B_[0] = b[0];
    C_[0] = c[0];
    D_[0] = d[0];


    for(int i=1;i<dim;i++){
        B_[i] = b[i]*B_[i-1]-C_[i-1]*a[i-1];
        if(i<dim-1){
            C_[i] = c[i]*B_[i-1];
        }
        D_[i] = d[i]*B_[i-1]-D_[i-1]*a[i-1];
    } 

    x[dim-1]=D_[dim-1]/B_[dim-1];
    for(int i=dim-2;-1<i;i--){
        x[i] = (D_[i]-C_[i]*x[i+1])/B_[i];
    }

    return x;
}



//#######################################################################################################
//###############------OPERADORES-------#################################################################
//#######################################################################################################



//SUMA DE MATRICES, PUEDEN TENER DISTINTAS DIMENSIONES
template <class T>
Matriz<T> operator+(const Matriz<T> & A ,const Matriz<T> & B ){

    // COPIAS 
    Matriz<T> temp_A = A;
    Matriz<T> temp_B = B;

    Matriz<T> C(int(temp_A.filas()),int(temp_A.columnas()));
    if (temp_A.filas() == temp_B.filas())
    {
        if(temp_A.columnas() == temp_B.columnas())
        {
            //Suma de matrices
            for(int i = 0; i < (int)temp_A.filas(); i++)
            {
                for(int j = 0; j < (int)temp_A.columnas(); j++)
                {
                    C(i,j) = temp_A(i,j) + temp_B(i,j);
                }       
            }
        }
        else
        {   
            temp_A.resize(temp_A.filas(), temp_B.columnas());
            temp_B.resize(temp_B.filas(), temp_A.columnas());
            C.resize(temp_A.filas(), temp_A.columnas());
            //Suma de matrices
            for(int i = 0; i < (int)temp_A.filas(); i++)
            {
                for(int j = 0; j < (int)temp_A.columnas(); j++)
                {
                    C(i,j) = temp_A(i,j) + temp_B(i,j);
                }       
            }
        }
        
    }
    else
    {
        if(temp_A.columnas() == temp_B.columnas())
        {
            temp_A.resize(temp_B.filas(), temp_A.columnas());
            temp_B.resize(temp_A.filas(), temp_B.columnas());
            C.resize(temp_A.filas(), temp_A.columnas());
            //Suma de matrices
            for(int i = 0; i < (int)temp_A.filas(); i++)
            {
                for(int j = 0; j < (int)temp_A.columnas(); j++)
                {
                    C(i,j) = temp_A(i,j) + temp_B(i,j);
                }       
            }
        }
        else
        {   
            temp_A.resize(temp_B.filas(), temp_B.columnas());
            temp_B.resize(temp_A.filas(), temp_A.columnas());
            C.resize(temp_A.filas(), temp_A.columnas());
            //Suma de matrices
            for(int i = 0; i < (int)temp_A.filas(); i++)
            {
                for(int j = 0; j < (int)temp_A.columnas(); j++)
                {
                    C(i,j) = temp_A(i,j) + temp_B(i,j);
                }       
            }
        }
        
    }
    return C;
} 

//RESTA DE MATRICES
template <class T>
Matriz<T> operator-(const Matriz<T> & A, const Matriz<T> & B){
    
    Matriz<T> C;
    for(int i = 0; i < (int)A.filas(); i++)
        {
            for(int j = 0; j < (int)A.columnas(); j++)
            {
                C(i,j) = A(i,j) - B(i,j);
            }       
        }
    return C;
}

//MULTIPLICACIÓN
template <class T>
Matriz<T> operator*(Matriz<T> A, Matriz<T> B){

    Matriz<T> C(int(A.filas()),int(B.columnas()));
    if(A.columnas() == B.filas())
    {
        for(int k = 0; k < (int)B.columnas(); k++)
        {
            for(int j = 0; j < (int)A.filas(); j++)
            {
                for(int i = 0; i < (int)A.columnas(); i++)
                {
                    C(j,k) += A(j,i) * B(i,k);
                }
            }
        }
    }
    return C;
}        

template<class T>
vector<T> operator * (Matriz<T> A, vector<T> v){
    int dim = A.filas();
    vector<T> C(dim);
    T sumatoria = 0;
    for(int i=0;i<dim;i++)
    {
        for(int k=0;k<dim;k++)
        {
            sumatoria+= A(i,k)*v[k];
        }
        C[i] = sumatoria;
        sumatoria = 0;
    }
    return C;
}

template<class T>
Vector<T> operator * (Matriz<T> A, Vector<T> v){
    int dim = A.filas();
    vector<T> C(dim);
    T sumatoria = 0;
    for(int i=0;i<dim;i++)
    {
        for(int k=0;k<dim;k++)
        {
            sumatoria+= A(i,k)*v[k];
        }
        C[i] = sumatoria;
        sumatoria = 0;
    }
    return C;
}



template<class T>
Matriz<T> operator * (Matriz<T> A, T k)
{
    int dimf = A.filas();
    int dimc = A.columnas();
    Matriz<T> C(dimf,dimc);
    for(int i=0;i<dimf;i++)
    {
        for(int j=0;j<dimc;j++)
        {
            C(i,j) = k*A(i,j);
        }
    }
    return C;
}

template<class T>
Matriz<T> operator * (T k, Matriz<T> A)
{
    int dimf = A.filas();
    int dimc = A.columnas();
    Matriz<T> C(dimf,dimc);
    for(int i=0;i<dimf;i++)
    {
        for(int j=0;j<dimc;j++)
        {
            C(i,j) = k*A(i,j);
        }
    }
    return C;
}

//ULTIMO CAMBIO

template<class T>
Matriz<T> operator * (Matriz<T> A, int k)
{
    int dimf = A.filas();
    int dimc = A.columnas();
    Matriz<T> C(dimf,dimc);
    for(int i=0;i<dimf;i++)
    {
        for(int j=0;j<dimc;j++)
        {
            C(i,j) = k*A(i,j);
        }
    }
    return C;
}

template<class T>
Matriz<T> operator * (int k, Matriz<T> A)
{
    int dimf = A.filas();
    int dimc = A.columnas();
    Matriz<T> C(dimf,dimc);
    for(int i=0;i<dimf;i++)
    {
        for(int j=0;j<dimc;j++)
        {
            C(i,j) = k*A(i,j);
        }
    }
    return C;
}

//CAMBIAR ELEMENTO FILA i, COLUMNA j
template <class T>
T & Matriz<T>::operator()(int i, int j){
    return matrix[i][j];
}

//OBTENER ELEMENTO FILA i, COLUMNA j
template <class T>
T Matriz<T>::operator()(int i, int j) const{
    return matrix[i][j];
}

//MOSTRAR EN PANTALLA
template <class T>
ostream & operator <<(ostream & os, Matriz<T> a)
{
    vector<vector<T>> x = a.get();
    os << "[";
    for(int i = 0; i < (int)x.size(); i++)
    {
        if(i==int(x.size()-1))
        {
            os << "{";
            for(int j = 0; j < (int)x[i].size();j++)
            {
                if(j==int(x[i].size()-1))
                {
                    cout<<x[i][j];
                }
                else
                {
                    cout << x[i][j] << ", ";
                }
            }
            os << "}]";
        }
        else
        {
            os << "{";
            for(int j = 0; j < (int)x[i].size();j++)
            {
                if(j==int(x[i].size()-1))
                {
                    cout<<x[i][j];
                }
                else
                {
                    cout << x[i][j] << ", ";
                }
            }
            os << "}," << "\n";
        }
    }
    return os;
}



//Se sobrecargan las operaciones +,-,*,/ para vectores de cualquier dimension de manera que cumplan con el algebra de vectores
//--------------------------------

template <class T>
vector<T> operator + (vector<T> A, vector<T> B){
  vector<T> V(A.size());
  for(int i=0;i<A.size();i++){
V[i] = A[i] + B[i];
}
return V;
}

template <class T>
vector<T> operator - (vector<T> A, vector<T> B){
  vector<T> V(A.size());
  for(int i=0;i<A.size();i++){
V[i] = A[i] - B[i];
}
return V;
}



template <class T>
vector<T> operator * (T k, vector<T> A){
  vector<T> V(A.size());
  for(int i=0;i<A.size();i++){
V[i] = k*A[i];
}
return V;
}

template <class T>
vector<T> operator * (vector<T> A, T k){
  vector<T> V(A.size());
  for(int i=0;i<A.size();i++){
V[i] = k*A[i];
}
return V;
}

template <class T>
vector<T> operator / (vector<T> A, T k){
    vector<T> V(A.size());
    for(int i=0; i<A.size() ; i++){
        V[i] = A[i]/k;
    }
    return V;
}

//Se sobrecarga el operador << para vectores 
//--------------------
template<class T>
ostream & operator << (ostream & os,vector<T> v){

    int dim = v.size();
    os << "( ";
    for(int i=0;i<dim-1;i++){
        os << v[i] << " , ";
    }
    os << v[dim-1] << " )";
    return os;
} 

//Se implementa la funcion punto que retorna el producto punto
//---------------------
template <class T>
T punto(vector<T> E, vector<T> B){
  int n = E.size();
  T sumatoria = 0;
  for(int i=0;i<n;i++){
    sumatoria+= E[i]*B[i];
  }
  return sumatoria;
}


//Se implementa la funcion producto cruz que retorna el producto cruz
//--------------------
template <class T>
vector<T> cruz(vector<T> E, vector<T> B){
  int n = E.size();
  vector<T> ExB;
  T sumatoria = 0;
  for(int k=0;k<n;k++){
  for(int i=0;i<n;i++){
    for(int j=0;j<n;j++){
      sumatoria += LeviCita(i,j,k)*E[i]*B[j];
    }
  }
  ExB.push_back(sumatoria);
  sumatoria = 0;
  }
  return ExB;
}


template<class T>
Matriz<T> Inversa_Gaussiana(Matriz<T> A)
{
    int filas = A.filas();
    int columnas = A.columnas();
    Matriz<T> I(columnas);

    for(int i = 0; i < filas; i++)
    {
        T pivote = A(i,i);
        cout << pivote<<endl;
        for(int k = 0; k < columnas; k++)
        {
            A(i,k) = A(i, k)/pivote;
            //lo mismo en la matriz I
            I(i,k) = I(i, k)/pivote;

        }
        for (int j = 0; j < columnas; j++)
        {
            if(i!=j)
            {
                double aux = A(j,i);
                for(int k = 0; k < columnas; k++)
                {
                    A(j, k) = A(j, k) - aux*A(i,k);
                    //lo mismo para I
                    I(j, k) = I(j, k) - aux*I(i,k);
                }
            }
          
        }
    }
    return I;
}



#endif