import matplotlib.pyplot as plt

def graficar_listas_en_columnas(lista_de_listas):
    num_sublistas = len(lista_de_listas)
    num_elementos = max(len(sublista) for sublista in lista_de_listas)

    plt.figure(figsize=(10, 6))
    for i, sublista in enumerate(lista_de_listas):
        x_values = [i] * len(sublista)
        y_values = sublista
        plt.scatter(x_values, y_values, label=f'Lista {i}')

    plt.xlabel('Índice de la Lista')
    plt.ylabel('Valor')
    plt.title('Gráfico de Listas en Columnas')
    plt.xticks(range(num_sublistas))
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Ejemplo de uso
lista_de_listas = [[2, 5, 8], [10, 15, 20, 25], [7, 14, 21, 28, 35]]
graficar_listas_en_columnas(lista_de_listas)


