import random

matrix_size = 5
quantity_wolves = 2
quantity_rabbits = 10
quantity_plants = 4
vida_inicial = 5
empty = "."
occupied = "occupied"


class Organism:
    def __init__(self, initial_health, symbol, x, y):
        self.initial_health = initial_health
        self.symbol = symbol
        self.x = x
        self.y = y
        self.alive = True

    def is_life(self):
        return self.alive and self.initial_health > 0
    
    def aging(self):
        self.initial_health -= 1
        if self.initial_health <= 0:
            self.alive = False

    def reproduce_organisms(self, matrix, organism_list, index=0):
        if self.initial_health < 10:
            return

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        if index >= len(directions):
            return

        dx, dy = directions[index]
        new_x, new_y = self.x + dx, self.y + dy

        if (0 <= new_x < matrix.n) and (0 <= new_y < matrix.n) and (matrix.cells[new_x][new_y] == empty):
            new_organism = type(self)(x=new_x, y=new_y)
            matrix.cells[new_x][new_y] = new_organism
            organism_list.append(new_organism)
            self.initial_health -= 5
            return

        self.reproduce_organisms(matrix, organism_list, index + 1)


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
    def generate_recursive_matrix(n, row=0, matrix=[]):
        if row == n:
            return matrix
        
        return Recursive.generate_recursive_matrix(n, row + 1, matrix + [[empty] * n])
    
    def is_empty(self, x, y):
        return self.cells[x][y] == empty

    def put_organisms(self, organism_class, quantity, created_organisms:list[Organism]=None):
        if created_organisms is None:
            created_organisms = []

        if quantity == 0:
            return created_organisms

        x = random.randint(0, self.n - 1)
        y = random.randint(0, self.n - 1)

        if self.is_empty(x, y):
            organism = organism_class(x, y)
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
            return self.show_matrix(row + 1, 0)
            
        
        celda = self.cells[row][column]
        if isinstance(celda, Organism):
            print(celda.symbol, end=' ')
        else:
            print(celda, end=' ')
        
        self.show_matrix(row, column + 1)
    
    def find_closest_food(self, predator: 'Organism', prey_type: "Organism"):
        x = predator.x
        y = predator.y

        def search_row(j=0, closest_prey=None, min_distance=100):
            if j == self.n:
                return closest_prey, min_distance
            cell = self.cells[x][j]
            if isinstance(cell, prey_type):
                distance = abs(j - y)
                if distance < min_distance:
                    min_distance = distance
                    closest_prey = (x, j)
            return search_row(j + 1, closest_prey, min_distance)
        
        def search_column(i=0, closest_prey=None, min_distance=100):
            if i == self.n:
                return closest_prey, min_distance
            cell = self.cells[i][y]
            if isinstance(cell, prey_type):
                distance = abs(i - x)
                if distance < min_distance:
                    min_distance = distance
                    closest_prey = (i, y)
            return search_column(i + 1, closest_prey, min_distance)

        closest_row, dist_row = search_row()
        closest_col, dist_col = search_column()

        if closest_row is None and closest_col is None:
            return None
        elif closest_row is None:
            return closest_col
        elif closest_col is None:
            return closest_row
        else:
            if dist_row <dist_col:
                return closest_row
            else:
                return closest_col
        
    def can_move_to_cell(self, organism, x, y):

        if not (0 <= x < self.n and 0 <= y < self.n):
            return False
        cell = self.cells[x][y]
        if cell == empty:
            return True
        if isinstance(organism, Wolf):
            return isinstance(cell, Rabbit)
        if isinstance(organism, Rabbit):
            return isinstance(cell, Plant)


    def move_entity(self, organism, target, prey_type):
        x, y = organism.x, organism.y
        new_x, new_y = x, y

        def try_moves(moves):
            if not moves:
                return (x, y)
            nx, ny = moves[0]
            if self.can_move_to_cell(organism, nx, ny):
                return (nx, ny)
            return try_moves(moves[1:])

        if target:
            tx, ty = target
            dx, dy = tx - x, ty - y
            posibles = []
            if dx > 0:
                posibles += [(x + 1, y)]
            if dx < 0:
                posibles += [(x - 1, y)]
            if dy > 0:
                posibles += [(x, y + 1)]
            if dy < 0:
                posibles += [(x, y - 1)]
            new_x, new_y = try_moves(posibles)

        if (new_x, new_y) == (x, y):
            dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(dirs)
            
            def build_moves(dirs, x, y, index=0):
                if index >= len(dirs):
                    return []
                move = (x + dirs[index][0], y + dirs[index][1])
                return [move] + build_moves(dirs, x, y, index + 1)
            
            moves = build_moves(dirs, x, y)
            new_x, new_y = try_moves(moves)

        if isinstance(self.cells[new_x][new_y], prey_type):
            self.cells[new_x][new_y].alive = False
            self.cells[new_x][new_y] = empty
            self.eat(organism)
            print(f" la vida del {organism} en la posición [{organism.x},{organism.y}] es de {organism.initial_health}")

        self.cells[x][y] = occupied
        organism.x, organism.y = new_x, new_y
        self.cells[new_x][new_y] = organism


    def move_wolf(self, wolf):
        closest_rabbit = self.find_closest_food(wolf, Rabbit)
        self.move_entity(wolf, closest_rabbit, Rabbit)

    def move_all_wolves(self, wolves, index=0):
        if index >= len(wolves):
            return
        if wolves[index].alive and self.cells[wolves[index].x][wolves[index].y] != empty:
            self.move_wolf(wolves[index])
        return self.move_all_wolves(wolves, index + 1)
        

    def move_rabbit(self, rabbit):
        if not rabbit.alive:
            return
        closest_plant = self.find_closest_food(rabbit, Plant)
        self.move_entity(rabbit, closest_plant, Plant)

    def move_all_rabbits(self, rabbits, index=0):
        if index >= len(rabbits):
            return
        if rabbits[index].alive and self.cells[rabbits[index].x][rabbits[index].y] != empty:
            self.move_rabbit(rabbits[index])
        self.move_all_rabbits(rabbits, index + 1)

    def clear_occupied(self, i=0, j=0):
        if i >= self.n:
            return

        if j >= self.n:
            self.clear_occupied(i + 1, 0)
            return

        if self.cells[i][j] == occupied:
            self.cells[i][j] = empty

        self.clear_occupied(i, j + 1)


    def eat(self, predator):
        predator.initial_health += 2

    def reproduce_all(matrix, organisms, index=0):
        if index >= len(organisms):
            return 
        organisms[index].reproduce_organisms(matrix, organisms) 
        return Recursive.reproduce_all(matrix, organisms, index + 1)


matrix = Recursive(matrix_size)
wolves = matrix.put_organisms(Wolf, quantity_wolves)
rabbits = matrix.put_organisms(Rabbit, quantity_rabbits)
plants = matrix.put_organisms(Plant, quantity_plants)

print("Estado inicial:")
matrix.show_matrix()
print()

def simulation_turn(matrix, wolves, rabbits, current_turn, max_turns):
    if current_turn > max_turns:
        return
    matrix.move_all_wolves(wolves)
    matrix.move_all_rabbits(rabbits)
    Recursive.reproduce_all(matrix, wolves)
    Recursive.reproduce_all(matrix, rabbits)
    matrix.clear_occupied()
    print("\nEstado después del turno", current_turn, ":")
    matrix.show_matrix()
    input("\nPresiona Enter para continuar...")
    simulation_turn(matrix, wolves, rabbits, current_turn + 1, max_turns)

input("Presiona Enter para iniciar la simulación...")
simulation_turn(matrix, wolves, rabbits, 1, 100) #ja


