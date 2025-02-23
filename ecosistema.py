import random

class Recursive:

    @staticmethod
    def generate_recursive_matrix(size:int, i:int =0, j:int=0, fila:list[int]=None, matrix: list[list[int]]= None):
        if fila == None and matrix == None:
            fila = []
            matrix = []
        if i == size: #Caso base cuando ya se tengan todas las filas en la matriz, se retorne la matriz
            return matrix
        if j == size: #Caso base para evaluar si ya estamos en la útlima celda de una fila
            matrix.append(fila)
            return Recursive.generate_recursive_matrix(size, i + 1, 0, [], matrix)

        random_organism = Recursive.generate_random_organism()
        fila.append(random_organism) #Agregar número aleatorio a la fila actual

        return Recursive.generate_recursive_matrix(size, i, j+1, fila, matrix)
    
    @staticmethod
    def generate_random_organism():
        organism = random.choice(['P', 'R', 'W', "-"])
        if organism == 'P':
            return Plant()
        elif organism == 'R':
            return Rabbit()
        elif organism == 'W':
            return Wolf()
        else: 
            return Null()
    
    @staticmethod
    def eat(self, matrix: list[list[int]], i: int, j: int):
        if matrix[i][j] == 1:
            self.initial_health += 1
        return self.initial_health


class Organism:
    def __init__(self, initial_health: int):
        self.initial_health: int = initial_health

    def is_life(self):
        return self.initial_health > 0
    
    def ageing(self):
        self.initial_health -= 1
        return self.initial_health#Comprobar si se necesita esta linea

class Wolf(Organism):
    def __init__(self):
        super().__init__(initial_health = 5)
    
    def __repr__(self):
        return "W"
    
    #def movement_matrix(self):
        

class Plant(Organism):
    def __init__(self):
        super().__init__(initial_health = 1)
    
    def __repr__(self):
        return "P"

class Rabbit(Organism):
    def __init__(self):
        super().__init__(initial_health = 3)
        
    def __repr__(self):
        return "R"

class Null(Organism):
    def __init__(self):
        super().__init__(initial_health = 0)
    
    def __repr__(self):
        return "-"
class Matrix:
    def __init__(self, size: int):
        self.size = size
        self.matriz = Recursive.generate_recursive_matrix(size)

    def show_format_matrix(self, i: int= 0):
        if i == self.size:
            return
        print(self.matriz[i])
        return self.show_format_matrix(i+1)

matriz = Matrix(5)
matriz.show_format_matrix()

