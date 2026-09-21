from mazegenerator import MazeGenerator
import pygame, sys
import random


def display(screen,generator,pos,food,super_pacgums):
    pygame.init()
    black = (0, 0, 0)
    width, height = screen.get_size()
    font = pygame.font.Font(None, 40)
    #suppose the arr has 15 col and row that why we will see if it change or not 
    cell_size = min(width//15,height//15)
    for row, line in enumerate(generator.maze):
        for col, cell in enumerate(line):
            x = col * cell_size
            y = row * cell_size
            pacman = font.render(".", True, (255, 255, 0))
            super_pacgum = font.render("#",True, (255,255,0))
            if not (cell &1 and cell & 2 and cell & 4 and cell & 8):
                if food is None:
                    screen.blit(pacman, (x+20, y+5))
                    food = [row.copy() for row in generator.maze]
                    food[0][0] = 20
                elif [row,col] in super_pacgums: 
                    screen.blit(super_pacgum,(x+20,y+5))
                    if [row,col] == [0,0] and [row,col] in super_pacgums:
                        super_pacgums.remove([0,0])
                elif generator.maze[row][col] == food[row][col]:
                    screen.blit(pacman, (x+20, y+5))
            # top
            if cell & 1:
                pygame.draw.line(screen, (100, 80, 120),(x, y),(x + cell_size, y), 3)
            # right
            if cell & 2:
                pygame.draw.line(screen, (100, 80, 120),(x + cell_size, y),(x + cell_size, y + cell_size), 3)
            # bottom
            if cell & 4:
                pygame.draw.line(screen, (100, 80, 120),(x, y + cell_size),(x + cell_size, y + cell_size), 3)
            # left
            if cell & 8:
                pygame.draw.line(screen, (100, 80, 120),(x, y),(x, y + cell_size), 3)
    return food,super_pacgums
            
#from now i will like just test that and i will start from 0,0 after that i will change it to the middle
def ft_check_walls(pos, row , col,generator):
    cell = generator.maze[row][col]
    
    if pos == [0,1]:
        if cell & 2:
            return False
    if pos == [0,-1]:
        if cell & 8:
            return False
    if pos == [1,0]:
        if cell & 4:
            return False
    if pos == [-1,0]:
        if cell & 1:
            return False
    return True
def ft_find_paths(generator,position_pacman,pos_ghost,directions,size):
    paths = []
    # paths.append(pos_ghost)
    current = []
    all_paths = []
    current_ghost_x = pos_ghost[0]
    current_ghost_y = pos_ghost[1]
    def recursion_dfs(path,current):
        # print("======>", current)
        if current == position_pacman:
            all_paths.append(path.copy())
        else:
            for x, y in directions:
                pos = [x, y]
                # pos_ghost[0] += x 
                # pos_ghost[1] += y
                current_ghost_x += x
                current_ghost_y += y
                current = [current_ghost_x, current_ghost_y]
                if current in path:
                    continue
                if 0 <= pos_ghost[0] <= size[0]-1 and 0 <= pos_ghost[1] <= size[1] -1:
                    if ft_check_walls(pos,pos_ghost[0]+x,pos_ghost[1]+y,generator):
                        path.append(current)
                        recursion_dfs(path,current)
                
        path.pop()

    recursion_dfs([],current)
    return all_paths



def ft_position_ghost(size,generator,position_pacman):
    directions = [[1,0],[-1,0],[0,-1],[0,1]]
    random_spot_x = random.randint(0,size[0]-1)
    random_spot_y = random.randint(0,size[1]-1)
    position_ghost = [random_spot_x,random_spot_y]

    ft_find_paths(generator,position_pacman,position_ghost,directions,size)


def main():
    screen = pygame.display.set_mode((800,800))

    width, height = screen.get_size()
    size_cell = min(width//15,height//15)
    start_to = 5
    # pacman = pygame.image.load("pacman_up.png")
    # screen.blit(pacman, (x, y))
    pygame.init()
    pos = None
    pending_pos = None
    character_pacman = "@"
    position_pacman = [0,0]
    checker_x = 0
    checker_y = 0
    background = (15, 15, 20)
    size=(15, 15)
    generator = MazeGenerator(
            size,
            perfect=False,
            entry_cell=(0, 0),
            exit_cell=(-1, -1),
            seed=0
        )

    super_pacgums = [[0,0],[0,size[1]-1],[size[0]-1,0],[size[0]-1,size[1]-1]]
    font = pygame.font.Font(None, 40)
    running = True
    pos= None
    directions = { 
        pygame.K_RIGHT :[0,1], 
        pygame.K_LEFT: [0,-1], 
        pygame.K_UP: [-1,0], 
        pygame.K_DOWN:[1,0] 
    }
    step_x = 0
    step_y = 0
    # random_spot_x = random.randint(0,size[0]-1)
    # random_spot_y = random.randint(0,size[1]-1)
    spot_ghost = ft_position_ghost(size, generator,position_pacman)
    x=0
    y=0
    food = None
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in directions:
                    pending_pos = directions[event.key]
        if pending_pos is not None and step_x == 0 and step_y == 0:
                pos = pending_pos
                pending_pos = None

        if pos:
            row = position_pacman[0]
            col = position_pacman[1]
            if ft_check_walls(pos,row,col,generator):
                step_x += pos[1] * 3
                step_y += pos[0] * 3
                if abs(step_x) >= size_cell:
                    step_x = 0
                    position_pacman[1] += pos[1]
                    if food:
                        food[row][position_pacman[1]] = 20
                        if [row,position_pacman[1]] in super_pacgums:
                            super_pacgums.remove([row,position_pacman[1]])
                
                if abs(step_y) >= size_cell:
                    step_y = 0
                    position_pacman[0] += pos[0]
                    if food:
                        food[position_pacman[0]][col] = 20
                        if [position_pacman[0],col] in super_pacgums:
                            print("iiiii eaat it also ",position_pacman[0],col)
                            super_pacgums.remove([position_pacman[0],col])
        x = (position_pacman[1] * size_cell) + step_x
        y = (position_pacman[0] * size_cell) + step_y
        screen.fill(background)
        food,super_pacgums = display(screen,generator,pos,food,super_pacgums)
        ghost = font.render("G", True,(0,0,0))
        # screen.blit(ghost,(,))
        pacman = font.render("@", True, (255, 255, 0))
        screen.blit(pacman, (x+10, y+10))
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()   
    sys.exit()

main()