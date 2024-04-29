import pygame
import math
from queue import PriorityQueue

# setting up the window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

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


# represents a node in the grid 
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

    # update the neighbour for all the nodes in given grid
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

# reconstruct the path from start to end after completion of the algorithm
def reconstruct_path_astr(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.change_state(GREEN)
        draw()

# A* algorithm
def astar_algorithm(draw, grid, start, end):
    draw()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())


    # just to keep track of what is in the priority queue as this is not provided by the priority queue
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current) # removing from hash as well

        # stop if reached the end
        if current == end:
            reconstruct_path_astr(came_from, end, draw)
            return True
        # each neighbours are just one node away and as we are using square grid, g_Score will be just +1
        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                # adding to the open_set if not already in it
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
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
            # key press event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    astar_algorithm(lambda:draw(win, grid, ROWS, width), grid, start, end)
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