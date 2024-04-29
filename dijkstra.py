import pygame
import math
from queue import PriorityQueue

# setting up the window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Dijkstra Shortest Path Finding Algorithm")

# defining color values for pygame
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def change_state(self, state):
        self.color = state

    # def make_start(self):
    #     self.color = ORANGE

    # def make_end(self):
    #     self.color = PURPLE

    # def make_barrier(self):
    #     self.color = BLACK

    def make_open(self):
        self.color = GREEN

    def make_closed(self):
        self.color = RED

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.row+1][self.col].is_barrier(): # DOWN
            self.neighbours.append(grid[self.row+1][self.col])
        if self.row > 0 and  not grid[self.row-1][self.col].is_barrier(): # UP
            self.neighbours.append(grid[self.row-1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col+1].is_barrier(): # LEFT
            self.neighbours.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid[self.row][self.col-1].is_barrier(): # RIGHT
            self.neighbours.append(grid[self.row][self.col-1])



    def __lt__(self, other):
        return False

# heuristic function(h value), uses manhattan distance
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x2 - x1) + abs(y2 - y1)

def reconstruct_path_astr(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.change_state(GREEN)
        draw()


def reconstruct_path_dj(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.change_state(GREEN)
        draw()

            

def dijkstra_algorithm(draw, grid, start, end):
    draw()
    count = 0
    cost = {node: float("inf") for row in grid for node in row}
    cost[start] = 0
    open_set = PriorityQueue()
    open_set.put((cost[start], count, start))
    came_from = {}
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path_dj(came_from, end, draw)
            return True

        for neighbour in current.neighbours:
            temp_cost = cost[current] + 1
            if temp_cost < cost[neighbour]:
                came_from[neighbour] = current
                cost[neighbour] = temp_cost

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((cost[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.change_state(YELLOW)

        draw()
        if current != start:
            current.change_state(RED)
    return False


# a function to make grid
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win , GREY, (0, i*gap), (width, i*gap))

    for j in range(rows):
        pygame.draw.line(win, GREY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def  get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col



def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]: # left button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.change_state(BLUE)

                elif node != start and not end:
                    end = node
                    end.change_state(ORANGE)
                
                elif node != start and node != end:
                    node.change_state(BLACK)

                    
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    dijkstra_algorithm(lambda:draw(win, grid, ROWS, width), grid, start, end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_r:
                    for row in grid:
                        for node in row:
                            if node != start and node != end:
                                node.change_state(BLACK)
                            
    pygame.quit()



if __name__ == "__main__":
    main(WIN, WIDTH)