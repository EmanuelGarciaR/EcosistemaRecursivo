import random

matrix_size = 4
quantity_wolves = 4
quantity_rabbits = 4  
quantity_plants = 4
vida_inicial = 5
empty = "."

class Organism:
    def __init__(self, initial_health: int, symbol, x: int, y: int):
        self.initial_health: int = initial_health
        self.symbol = symbol
        self.x = x
        self.y = y

    def is_life(self):
        return self.initial_health > 0
    
    def aging(self):
        self.initial_health -= 1
        return self.initial_health

    def move_towards(self, target_x, target_y):
        new_x, new_y = self.x, self.y

        if self.x < target_x:
            new_x += 1
        elif self.x > target_x:
            new_x -= 1

        if self.y < target_y:  # Quitamos el `elif`
            new_y += 1
        elif self.y > target_y:
            new_y -= 1

        return new_x, new_y



class Wolf(Organism):

    def __init__(self, x: int, y:int):
        super().__init__(initial_health=5, symbol="W", x=x, y=y)
    
    def __repr__(self):
        return "W"
    
class Plant(Organism):
    def __init__(self, x, y):
        super().__init__(initial_health=3, symbol="P", x=x, y=y)
    
    def __repr__(self):
        return "P"

    def move_towards(self, **_):
        return ":)"

class Rabbit(Organism):
    def __init__(self, x, y):
        super().__init__(initial_health=3, symbol="R", x=x, y=y)
        
    def __repr__(self):
        return "R"

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

    def put_organisms(self, organism_class, quantity, created_organisms=None):
        if created_organisms is None:
            created_organisms = []

        if quantity == 0:
            return created_organisms

        x = random.randint(0, self.n - 1)
        y = random.randint(0, self.n - 1)

        if self.is_empty(x, y):
            organism = organism_class(x, y)
            #print(f"Colocando {organism_class.__name__} en ({x}, {y})") -> Depuración
            self.cells[x][y] = organism
            created_organisms.append(organism)

            return self.put_organisms(organism_class, quantity - 1, created_organisms)
        else:
            return self.put_organisms(organism_class, quantity, created_organisms)

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
    
    def find_closest_organism(self, predator, prey_class, row=0, col=0, best=None, min_distance=float('inf')):
        if row >= self.n:
            if best:
                return best[0]
            return None

        if col >= self.n:
            return self.find_closest_organism(predator, prey_class, row + 1, 0, best, min_distance)

        cell = self.cells[row][col]

        # Depuración: Ver qué hay en cada celda
        #print(f"Revisando celda ({row}, {col}): {cell}")

        if isinstance(cell, prey_class):
            #print(f"Encontrado {prey_class.__name__} en ({row}, {col})") #Depuración

            predator_pos = (predator.x, predator.y)
            prey_pos = (row, col)
            distance = abs(predator_pos[0] - prey_pos[0]) + abs(predator_pos[1] - prey_pos[1])
            #print(f"La distancia es {distance}") -> Depuración

            if distance < min_distance:
                best = (cell, distance) #Acceder a la menor distancia en best[1]
                min_distance = distance  # Actualizar la menor distancia encontrada

        return self.find_closest_organism(predator, prey_class, row, col + 1, best, min_distance)

    def move_organism(self, predator:Organism, prey_class: Organism):
        """Mueve el organismo (predador) hacia la presa más cercana en la matriz."""
        prey = self.find_closest_organism(predator, prey_class)
        
        if not prey:
            print(f"{predator.symbol} en ({predator.x}, {predator.y}) no encontró presa.")
            return

        print(f"{predator.symbol} en ({predator.x}, {predator.y}) se mueve hacia {prey.symbol} en ({prey.x}, {prey.y})")
        
        #Guardar posición anterior
        prev_x, prev_y = predator.x, predator.y

        #Calcular la siguiente posición sin mover directamente
        new_x, new_y = predator.move_towards(prey.x, prey.y)

        target_cell = self.cells[new_x][new_y]
        
        if target_cell is empty or isinstance(target_cell, prey_class):
            # Mover el predador un paso hacia la presa
            predator.x, predator.y = new_x, new_y

            # Actualizar la matriz
            self.cells[prev_x][prev_y] = empty  # Dejar vacía la posición anterior
            self.cells[predator.x][predator.y] = predator  # Colocar el predador en la nueva posición
        
        # Si llegó a la presa, la come
        if predator.x == prey.x and predator.y == prey.y:
            self.eat(predator, prey)
        else:
            print(f"{predator.symbol} en ({predator.x}, {predator.y} no puede moverse porque ({new_x}, {new_y}) está ocupado.)")
    
    def eat(self, predator, prey):
        """El predador consume la presa y gana vida."""
        print(f"{predator.symbol} en ({predator.x}, {predator.y}) ha comido a {prey.symbol}.")
        predator.initial_health += 2  # Incrementar vida del depredador
        self.cells[predator.x][predator.y] = predator  # Actualizar la matriz


# Crear la matriz y colocar los organismos
matrix = Recursive(matrix_size)
wolves = matrix.put_organisms(Wolf, quantity_wolves)
rabbits = matrix.put_organisms(Rabbit, quantity_rabbits)
plants = matrix.put_organisms(Plant, quantity_plants)

# Mostrar la matriz inicial
print("\nEstado inicial de la matriz:")
matrix.show_matrix()

# Seleccionar un lobo aleatorio
wolf = random.choice(wolves)
print(f"La vida del lobo es: {wolf.initial_health}")

# Mover el lobo y hacer que cace
while True:
    closest_rabbit = matrix.find_closest_organism(wolf, Rabbit)
    
    if not closest_rabbit:
        print("No quedan más conejos en la matriz.")
        break

    matrix.move_organism(wolf, Rabbit)
    matrix.show_matrix()  # Mostrar la matriz tras cada movimiento

    # Verificar si el lobo ha alcanzado al conejo
    if wolf.x == closest_rabbit.x and wolf.y == closest_rabbit.y:
        print(f"El lobo en ({wolf.x}, {wolf.y}) ha comido al conejo.")
        print(f"La vida del lobo es: {wolf.initial_health}")
        break



