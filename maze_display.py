from mazegenerator import MazeGenerator
import pygame, sys
import random
import time

class Render:
    def __init__(self, size,size_cell,screen,directions,generator,len_path):
        self.size = size
        self.size_cell = size_cell
        self.screen = screen
        self.directions = directions
        self.generator = generator
        self.len_path = len_path
    def display(self,pos,food,super_pacgums):
        pygame.init()
        black = (0, 0, 0)
        font = pygame.font.Font(None, 40)
        cell_size = self.size_cell
        for row, line in enumerate(self.generator.maze):
            for col, cell in enumerate(line):
                x = col * cell_size
                y = row * cell_size
                pacman = font.render(".", True, (255, 255, 0))
                super_pacgum = font.render("#",True, (255,255,0))
                if not (cell &1 and cell & 2 and cell & 4 and cell & 8):
                    if food is None:
                        self.screen.blit(pacman, (x+20, y+5))
                        food = [row.copy() for row in self.generator.maze]
                        food[0][0] = 20
                    elif [row,col] in super_pacgums: 
                        self.screen.blit(super_pacgum,(x+20,y+5))
                        if [row,col] == [0,0] and [row,col] in super_pacgums:
                            super_pacgums.remove([0,0])
                    elif self.generator.maze[row][col] == food[row][col]:
                        self.screen.blit(pacman, (x+20, y+5))
                # top
                if cell & 1:
                    pygame.draw.line(self.screen, (100, 80, 120),(x, y),(x + cell_size, y), 3)
                # right
                if cell & 2:
                    pygame.draw.line(self.screen, (100, 80, 120),(x + cell_size, y),(x + cell_size, y + cell_size), 3)
                # bottom
                if cell & 4:
                    pygame.draw.line(self.screen, (100, 80, 120),(x, y + cell_size),(x + cell_size, y + cell_size), 3)
                # left
                if cell & 8:
                    pygame.draw.line(self.screen, (100, 80, 120),(x, y),(x, y + cell_size), 3)
        return food,super_pacgums
                
    #from now i will like just test that and i will start from 0,0 after that i will change it to the middle
    def ft_check_walls(self,pos, row , col):
        cell = self.generator.maze[row][col]
        
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


    def ft_find_paths(self,position_pacman,pos_ghost):
        paths = []
        directions = self.directions
        current = [pos_ghost[0],pos_ghost[1]]
        all_paths = []
        def recursion_dfs(path,current):
            # print("======>", current)
            if current == position_pacman:
                all_paths.append(path.copy())
                return
            else:
                for x, y in directions:
                    pos = [x, y]
                    if [current[0]+x ,current[1]+y] in path:
                        continue
                    if 0 <= current[0] <= self.size[0]-1 and 0 <= current[1] <= self.size[1] -1:
                        if self.ft_check_walls(pos,current[0],current[1]):
                            path.append(current)
                            recursion_dfs(path,[current[0]+x, current[1]+y])
                            path.pop()

        recursion_dfs([],current)
        return all_paths



    def ft_position_ghost(self,position_pacman,position_ghost):
        r = self.size[0]//4
        c = self.size[1]//4
        check = False
        for i in range(20):
            random_spot_x = random.randint(r*1,r*3)
            random_spot_y = random.randint(c*1,c*3)
            for i in self.directions:
                if self.ft_check_walls(i ,random_spot_x,random_spot_y):
                    check = True
                    break
        if check == False:
            for i in range(300):
                random_spot_x = random.randint(0,self.size[0])
                random_spot_y = random.randint(0,slef.size[1])
                for i in self.directions:
                    if self.ft_check_walls(i ,random_spot_x,random_spot_y):
                        check = True
                        break
        if check == False:
            print("hereeeeeeee should i raise error :)")
        if check == True:    
            position_ghost = [random_spot_x,random_spot_y]
            paths = self.ft_find_paths(position_pacman,position_ghost)
        return [random_spot_x,random_spot_y],paths

        return paths
    def ft_render_paths_debug(self,paths, show_path, p):
        n = [(255, 255, 255), (255, 0, 0), (0, 255, 0),
            (0, 255, 255), (255, 215, 0)]
        if not paths:
            return p
        if show_path and p < len(paths):
            for y in paths[p]:
                row = y[0]
                col = y[1]

                font = pygame.font.Font(None, 40)
                path = font.render("P", True, n[p % len(n)])
                self.screen.blit(path, ((col * self.size_cell) + 5,(row * self.size_cell) + 10))
            p += 1

        return p
    def move_ghost(self, ghost_x,ghost_y,paths,p):
        if not paths:
            return ghost_x,ghost_y,p
        if len(paths[self.len_path]) <= p:
            self.len_path +=1
            p = 0

        if self.len_path >= len(paths):
            self.len_path = 0
            p = 0
        y = paths[self.len_path][p]
        row = y[0]
        col = y[1]
        print("here==>",y)
        ghost_x += row - ghost_x
        ghost_y += col - ghost_y
        p+=1
        return ghost_x,ghost_y,p



def main():
    screen = pygame.display.set_mode((800,800))
    p = 0
    show_path = False

    pygame.init()
    pos = None
    pending_pos = None
    character_pacman = "@"
    position_pacman = [0,0]
    background = (15, 15, 20)
    size=(8, 8)
    generator = MazeGenerator(
            size,
            perfect=False,
            entry_cell=(0, 0),
            exit_cell=(-1, -1),
            seed=0
        )
    directions_wall = [[1,0],[-1,0],[0,-1],[0,1]]
    width, height = screen.get_size()
    size_cell = min(width//size[0],height//size[1])
    render = Render(size, size_cell, screen,directions_wall,generator,0)
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
    p = 0
    position_ghost = [0,0]
    paths = []
    position_ghosts,paths = render.ft_position_ghost(position_pacman,position_ghost)
    ghost_x = position_ghosts[0]
    ghost_y = position_ghosts[1]
    x = 0
    y = 0
    food = None
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in directions:
                    pending_pos = directions[event.key]
                if event.key == pygame.K_SPACE:
                    show_path = True
        if pending_pos is not None and step_x == 0 and step_y == 0:
                pos = pending_pos
                pending_pos = None
        
        if pos:
            row = position_pacman[0]
            col = position_pacman[1]
            if render.ft_check_walls(pos,row,col):
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
                            print("iiiii eaat it also",position_pacman[0],col)
                            super_pacgums.remove([position_pacman[0],col])
        ghost_x,ghost_y,p = render.move_ghost(ghost_x,ghost_y,paths,p)
        x = (position_pacman[1] * size_cell) + step_x
        y = (position_pacman[0] * size_cell) + step_y
        screen.fill(background)
        food,super_pacgums = render.display(pos,food,super_pacgums)
        ghost = font.render("G", True, (255, 255, 255))
        screen.blit(ghost,(ghost_y*size_cell,ghost_x*size_cell))
        pacman = font.render("@", True, (255, 255, 0))
        screen.blit(pacman, (x+10, y+10))
        p = render.ft_render_paths_debug(paths,show_path,p)
        pygame.time.get_ticks()

        show_path = False
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()   
    sys.exit()

main()