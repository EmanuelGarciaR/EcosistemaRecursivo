import random

matrix_size = 5
quantity_wolves = 3
quantity_rabbits = 2
quantity_plants = 2
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

    def put_organisms(self, organism_class, quantity):
        if quantity == 0:
            return
        
        x = random.randint(0, self.n - 1)
        y = random.randint(0, self.n - 1)
        
        if self.is_empty(x, y):
            if organism_class == Wolf:
                organism = Wolf(x,y)
            # elif organism_class == Rabbit:
            #     organism = Rabbit(x,y)
            else:
                organism = organism_class()
            self.cells[x][y] = organism
            self.put_organisms(organism_class, quantity-1)
        else:
            self.put_organisms(organism_class, quantity)

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
    
    def find_closest_rabbit(self, x, y):
        #X , Y posición del lobo
        #j es para la fila
        def search_row(x: int, y:int, j: int = 0, clossest_rabbit: tuple[int, int]=None, min_distance: int = 10000):
            if j == self.n:
                return clossest_rabbit, min_distance
            
            if isinstance(self.cells[x][j], Rabbit):
                distance = abs(j - y)
                if distance < min_distance:
                    min_distance = distance
                    clossest_rabbit = (x,j)
            return search_row(x, y, j+1, clossest_rabbit, min_distance)
        
        def search_column(x: int, y:int, i: int = 0, clossets_rabbit: tuple[int, int]= None, min_distance: int = 10000):
            if i == self.n:
                return clossets_rabbit, min_distance
            
            if isinstance(self.cells[i][y], Rabbit):
                distance = abs(i - x)
                if distance < min_distance:
                    min_distance = distance
                    clossets_rabbit = (i, y)
            return search_column(x, y, i+1, clossets_rabbit, min_distance)

        closest_rabbit_row, min_distance_row = search_row(x, y)
        closest_rabbit_column, min_distance_column = search_column(x, y)

        if min_distance_row < min_distance_column:
            return closest_rabbit_row
        else:
            return closest_rabbit_column

    def move_wolf(self, wolf):
        closest_rabbit = self.find_closest_rabbit(wolf.x, wolf.y)
        if closest_rabbit:
            target_x, target_y = closest_rabbit
            #Borrar la posición actual del wolf
            self.cells[wolf.x][wolf.y] = empty

            #Mover el wolf al rabbit más cercano
            wolf.move_towards(target_x, target_y)

            #Actualizar la matriz con la nueva posición del wolf
            self.cells[wolf.x][wolf.y] = wolf
            
    def move_all_wolves(self, i:int = 0, j:int = 0):
        if i == self.n:
            return

        if j == self.n:
            self.move_all_wolves(i+1, 0)
            return
        
        if isinstance(self.cells[i][j], Wolf):
            self.move_wolf(self.cells[i][j])
        
        self.move_all_wolves(i, j+1)

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
    def __init__(self, x: int, y:int):
        super().__init__(initial_health=5, symbol="W")
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "W"
    
    def move_towards(self, target_x, target_y):
        if self.x < target_x:
            self.x +=1
        elif self.x > target_x:
            self.x -= 1

        if self.y < target_y:
            self.y +=1
        elif self.y > target_y:
            self.y -= 1



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

# matrix = Recursive(matrix_size)
# matrix.put_organisms(Wolf(), quantity_wolves)
# matrix.put_organisms(Rabbit(), quantity_rabbits)
# matrix.put_organisms(Plant(), quantity_plants)
# print("Estado inicial: ")
# print(Recursive.find_closest_rabbit(2,2))
# matrix.show_matrix()

# Ejemplo de uso
matrix = Recursive(matrix_size)
matrix.put_organisms(Wolf, quantity_wolves)
matrix.put_organisms(Rabbit, quantity_rabbits)
matrix.put_organisms(Plant, quantity_plants)

print("Estado inicial: ")
matrix.show_matrix()

# Mover todos los lobos hacia los conejos más cercanos
matrix.move_all_wolves()

print("Estado después de mover los lobos: ")
matrix.show_matrix()


