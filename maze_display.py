from mazegenerator import MazeGenerator
from collections import deque
import pygame, sys
import random
import time

class Player:
    def __init__(self, size, size_cell,screen,directions,generator,len_path,speed_x,speed_y,n):
        self.size = size
        self.size_cell = size_cell
        self.screen = screen
        self.directions = directions
        self.generator = generator
        self.len_path = len_path
        self.speed_ghost_x = speed_x
        self.speed_ghost_y = speed_y
        self.n = n
        
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
    def ft_find_paths_bfs(self,position_pacman,pos_ghost):
        paths = []
        directions = self.directions
        prev = [0, 0]
        queue = {}
        visited = set() 
        current = [pos_ghost[0],pos_ghost[1]]
        visited.add(tuple(current))
        to_visit = deque([current]) 
        while to_visit:
            current = to_visit.popleft()
            if current == [position_pacman[0], position_pacman[1]]:
                break
            neighbors = []
            for i in directions:
                x, y = i
                nx, ny = current[0] - x, current[1] - y
                move = [nx - current[0], ny - current[1]]
                if nx < 0 or ny < 0 or nx > self.size[0] - 1 or ny > self.size[1] - 1:
                    continue

                if (nx, ny) in visited or not self.ft_check_walls(move, current[0], current[1]):
                    continue
                neighbors.append([nx, ny])
            for n in neighbors:
                visited.add(tuple(n))
                queue[tuple(n)] = tuple(current)
                to_visit.append(n)

        res = []
        prevs = (position_pacman[0], position_pacman[1])
        res.append(list(prevs))
        if tuple(prevs) not in queue:
            print("it go here and it reached here before it contunie",queue)
            return []
        curr = prevs
        while curr in queue:
            curr = queue[curr]
            res.append(list(curr))

        res.reverse()
        print("i thing should be here ",res)
        return res



class Ghost:
    def __init__(self, size, size_cell,screen,directions,generator,len_path,speed_x,speed_y,function,p,paths,counter):
        self.size = size
        self.size_cell = size_cell
        self.screen = screen
        self.directions = directions
        self.generator = generator
        self.len_path = len_path
        self.speed_ghost_x = speed_x
        self.speed_ghost_y = speed_y
        self.func = function
        self.p = p
        self.paths = paths
        self.counter = counter


    def ft_position_ghost(self,position_pacman,position_ghost):
        paths = self.func.ft_find_paths_bfs(position_pacman,position_ghost)
        print("======>befoooooooooooooooore",position_pacman)
        print("the paths is heeeeeeeeeere",paths)
        return position_ghost,paths

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
    
    def move_ghost(self, ghost_x,ghost_y):

        if not self.paths:
            print("there is no path to go on it")
            return ghost_x, ghost_y, [0, 0]
        if self.counter == 4:
            self.p = 0
            self.counter = 0 
        if len(self.paths) < self.len_path:
            print("the len it change it like it len of the path is < len_path")
            self.len_path = 0
        if self.p < len(self.paths):
            self.p+= 1
        if self.p >= len(self.paths):
            print("it gooooo here")
            self.p = 0

        next_node = self.paths[self.p]
        target_row, target_col = next_node[0], next_node[1]
        

        pos_row = target_row - ghost_y 
        pos_col = target_col - ghost_x

        return ghost_x, ghost_y, [pos_row, pos_col]
   
  
    def ft_speed_ghost(self,ghost_x,ghost_y,pos,position_pacman):
        if pos is None:
            self.counter += 1
            if self.counter == 4:
                position_ghosts,paths = self.ft_position_ghost(position_pacman,[ghost_y,ghost_x])
                self.paths = paths
            ghost_x,ghost_y,pos = self.move_ghost(ghost_x,ghost_y)
        if pos[0] != 0:
            self.speed_ghost_y += pos[0]*1

        if pos[1] != 0:
            self.speed_ghost_x += pos[1]*1
        
        if abs(self.speed_ghost_x) >= self.size_cell:
            ghost_x += pos[1]
            self.speed_ghost_x = 0
            pos = None

        elif abs(self.speed_ghost_y) >= self.size_cell:
            ghost_y += pos[0]
            self.speed_ghost_y = 0
            pos = None
           
        return self.speed_ghost_x,self.speed_ghost_y ,ghost_x, ghost_y,pos


class Display:
    def __init__(self):
        pass

    def run(self):
        p = 1
        show_path = False

        pygame.init()
        pos = None
        pending_pos = None
        character_pacman = "@"
        position_pacman = [0, 0]
        background = (15, 15, 20)
        speed_ghostx=0
        speed_ghosty=0
        size=(14, 14)
        move = False
        paths = []
        generator = MazeGenerator(
                size,
                perfect=False,
                entry_cell=(0, 0),
                exit_cell=(-1, -1),
                seed=0
            )
        
        directions_wall = [[1,0],[-1,0],[0,-1],[0,1]]
        screen = pygame.display.set_mode((size[1]*50,size[0]*50))
        width, height = screen.get_size()
        size_cell = min(width//size[1],height//size[0])
        speed_x = 0
        speed_y = 0
        counter = 0
        render = Player(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,0)
        ghost_func = Ghost(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,render,0,paths,counter)
        super_pacgums = [[0,0],[0,size[1]-1],[size[0]-1,0],[size[0]-1,size[1]-1]]
        font = pygame.font.Font(None, 40)
        running = True
        pos= None
        new = False

        directions = { 
            pygame.K_RIGHT :[0,1], 
            pygame.K_LEFT: [0,-1], 
            pygame.K_UP: [-1,0], 
            pygame.K_DOWN:[1,0] 
        }

        step_x = 0
        step_y = 0
        po_s = None
        

        position_ghost = [size[0]-1,size[1]-1]
        position_ghosts,paths = ghost_func.ft_position_ghost(position_pacman,position_ghost)
        ghost_func.paths = paths
     
        ghost_x = position_ghost[1]
        ghost_y = position_ghost[0]
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
                    print("$$$$=>the debug is position of the ghost",ghost_x,ghost_y)
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
                        # move = True
                        # position_ghosts,paths = ghost_func.ft_position_ghost(position_pacman,[ghost_x,ghost_y])
                        if food:
                            food[row][position_pacman[1]] = 20
                            if [row,position_pacman[1]] in super_pacgums:
                                super_pacgums.remove([row,position_pacman[1]])
                    if abs(step_y) >= size_cell:
                        step_y = 0
                        position_pacman[0] += pos[0]
                        # move = True
                        # position_ghosts,paths = ghost_func.ft_position_ghost(position_pacman,[ghost_x,ghost_y])
                        if food:
                            food[position_pacman[0]][col] = 20
                            if [position_pacman[0],col] in super_pacgums:
                                super_pacgums.remove([position_pacman[0],col])

            speed_ghostx,speed_ghosty,ghost_x,ghost_y,po_s = ghost_func.ft_speed_ghost(ghost_x,ghost_y,po_s,position_pacman)
            x = (position_pacman[1] * size_cell) + step_x
            y = (position_pacman[0] * size_cell) + step_y

            screen.fill(background)
            food,super_pacgums = render.display(pos,food,super_pacgums)
            
            ghost = font.render("G", True, (255, 255, 255))
            screen.blit(ghost,((ghost_x*size_cell)+speed_ghostx+10,(ghost_y*size_cell)+speed_ghosty+10))
            
            pacman = font.render("@", True, (255, 255, 0))
            screen.blit(pacman, (x+10, y+10))
            
            p = ghost_func.ft_render_paths_debug(paths,show_path,p)
            pygame.time.get_ticks()

            show_path = False
            pygame.display.flip()
            
            clock.tick(60)

        pygame.quit()   
        sys.exit()

if __name__ == "__main__":
    Display().run()