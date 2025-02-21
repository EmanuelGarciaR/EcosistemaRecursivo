import random

class Recursive:
    def __init__(self):
        pass
    @staticmethod
    def generate_recursive_matriz(size:int, i:int =0, j:int=0, fila:list[int]=None, matrix: list[list[int]]= None):
        if fila == None and matrix == None:
            fila = []
            matrix = []
        if i == size: #Caso base cuando ya se tengan todas las filas en la matriz, se retorne la matriz
            return matrix
        if j == size: #Caso base para evaluar
            matrix.append(fila)  # Agregar la fila completa a la matriz
            return Recursive.generate_recursive_matriz(size, i + 1, 0, [], matrix)  # Reiniciar j y fila para la siguiente fila

        fila.append(random.randint(1,7)) #Agregar número aleatorio a la fila actual

        return Recursive.generate_recursive_matriz(size, i, j+1, fila, matrix)


class Matriz:
    def __init__(self, size: int):
        self.size = size
        self.matriz = Recursive.generate_recursive_matriz(size)

    def show_format_matrix(self, i: int= 0):
        if i == self.size:
            return
        print(self.matriz[i])
        return self.show_format_matrix(i+1)


matriz = Matriz(5)
matriz.show_format_matrix()

