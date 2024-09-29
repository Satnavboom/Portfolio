import random
import time
from colorama import Fore, Style, init

init(autoreset=True)

COLOUR_O = Fore.RED
COLOUR_RED = Fore.RED
COLOUR_GREEN = Fore.GREEN
COLOUR_RESET = Style.RESET_ALL

game_ended = False

print()
grid_width = int(input("Width of grid: "))
grid_height = int(input("Height of grid: "))
total_cells = grid_width * grid_height

starting_live_cells = float('inf')
while starting_live_cells > total_cells or starting_live_cells < 1:
    starting_live_cells = int(input("Number of live cells: "))
    if starting_live_cells > total_cells:
        print(f"Too many cells, maximum number for your grid size is: {total_cells}")
    if starting_live_cells < 1:
        print("There must be at least one live cell")

grid = [['x' for _ in range(grid_width)] for _ in range(grid_height)]

live_cells_positions = random.sample(range(total_cells), starting_live_cells)

for pos in live_cells_positions:
    row = pos // grid_width
    col = pos % grid_width
    grid[row][col] = 'o'

def count_live_neighbours(grid, x, y, grid_width, grid_height) -> int:
    live_neighbours = 0
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            
            neighbour_x = x + i
            neighbour_y = y + j
            
            if 0 <= neighbour_x < grid_height and 0 <= neighbour_y < grid_width:
                if grid[neighbour_x][neighbour_y] == 'o':
                    live_neighbours += 1

    return live_neighbours

def apply_rules(grid, grid_width, grid_height) -> list:
    new_grid = [row[:] for row in grid]
    
    for x in range(grid_height):
        for y in range(grid_width):
            live_neighbours = count_live_neighbours(grid, x, y, grid_width, grid_height)
            
            if grid[x][y] == 'o':
                if live_neighbours < 2 or live_neighbours > 3:
                    new_grid[x][y] = 'x'
            
            elif grid[x][y] == 'x':
                if live_neighbours == 3:
                    new_grid[x][y] = 'o'
    
    return new_grid

def grid_to_string(grid) -> str:
    grid_str = ''
    for row in grid:
        row_str = ' '.join(COLOUR_O + cell + COLOUR_RESET if cell == 'o' else cell for cell in row)
        grid_str += row_str + '\n'
    return grid_str

iterations = 0
previous_states = set()
cell_counts = []

previous_cells_count = sum(cell == 'o' for row in grid for cell in row)
cell_counts.append(previous_cells_count)

while not game_ended:
    grid = apply_rules(grid, grid_width, grid_height)
    grid_str = grid_to_string(grid)
    
    live_cells_count = sum(cell == 'o' for row in grid for cell in row)
    cell_counts.append(live_cells_count)
    
    if grid_str in previous_states:
        print("\nDetected a repeating pattern. Ending the game.")
        iterations -= 1
        break
    
    previous_states.add(grid_str)
    
    
    iterations += 1
    
    if all(cell == 'x' for row in grid for cell in row):
        game_ended = True
    
    print("\033[H\033[J", end="")
    print(COLOUR_RED + f"\nGrid size: {grid_width}x{grid_height}" + COLOUR_RESET + f"         Cells: {(COLOUR_RED if previous_cells_count > live_cells_count else COLOUR_GREEN) + str(live_cells_count)}{COLOUR_RESET}/{total_cells}\n")
    print(grid_str)
        
    previous_cells_count = live_cells_count
    
    time.sleep(0.02)

print(f"Game ended in {COLOUR_RED + str(iterations) + COLOUR_RESET} iterations.\n")
