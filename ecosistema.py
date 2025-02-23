import random

matrix_size = 10
quantity_wolves = 2
quantity_rabbits = 5
quantity_plants = 10
vida_inicial = 5
empty = "."

class Recursive:
    def __init__(self, n):
        self.n = n
        self.cells = self.generate_recursive_matrix(n)

    @staticmethod
    def generate_recursive_matrix(n, row=0, matrix=None):
        if matrix is None:
            matrix = []
        if row == n:
            return matrix
        
        return Recursive.generate_recursive_matrix(n, row + 1, matrix + [[empty] * n])
    
    def is_empty(self, x, y):
        return self.cells[x][y] == empty

    def put_organisms(self, organism, quantity):
        if quantity == 0:
            return
        
        x = random.randint(0, self.n - 1)
        y = random.randint(0, self.n - 1)
        
        if self.is_empty(x, y):
            self.cells[x][y] = organism
            self.put_organisms(organism, quantity - 1)
        else:
            self.put_organisms(organism, quantity)
        
    def show_matrix(self, row=0, column=0):
        if row >= self.n:
            return
        
        if column >= self.n:
            print()
            self.show_matrix(row + 1, 0)
            return
        
        celda = self.cells[row][column]
        if isinstance(celda, Organism):
            print(celda.symbol, end=' ')
        else:
            print(celda, end=' ')
        
        self.show_matrix(row, column + 1)


class Organism:
    def __init__(self, initial_health: int, symbol):
        self.initial_health: int = initial_health
        self.symbol = symbol

    def is_life(self):
        return self.initial_health > 0
    
    def ageing(self):
        self.initial_health -= 1
        return self.initial_health


class Wolf(Organism):
    def __init__(self):
        super().__init__(initial_health=5, symbol="W")
    
    def __repr__(self):
        return "W"


class Plant(Organism):
    def __init__(self):
        super().__init__(initial_health=1, symbol="P")
    
    def __repr__(self):
        return "P"


class Rabbit(Organism):
    def __init__(self):
        super().__init__(initial_health=3, symbol="R")
        
    def __repr__(self):
        return "R"

matrix = Recursive(matrix_size)
matrix.put_organisms(Wolf(), quantity_wolves)
matrix.put_organisms(Rabbit(), quantity_rabbits)
matrix.put_organisms(Plant(), quantity_plants)
matrix.show_matrix()

