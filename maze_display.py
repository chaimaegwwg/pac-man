from mazegenerator import MazeGenerator
from collections import deque
import pygame, sys
import random
import time

class Player:
    def __init__(self, size, size_cell,screen,directions,generator,len_path,speed_x,speed_y,n,normal_pel,supper_pel):
        self.size = size
        self.size_cell = size_cell
        self.screen = screen
        self.directions = directions
        self.generator = generator
        self.len_path = len_path
        self.speed_ghost_x = speed_x
        self.speed_ghost_y = speed_y
        self.n = n
        self.normal_bel = normal_pel
        self.supper_pel = supper_pel
        
    def display(self,pos,food,super_pacgums):
        pygame.init()
        black = (0, 0, 0)
        font = pygame.font.Font(None, 40)
        cell_size = self.size_cell
        # normal_pel = pygame.image.load("image/normal_bel.png")
        # normal_pel = pygame.transform.scale(normal_pel,(80,45))
        # supper_pel = pygame.image.load("image/supper_bel.png")
        # supper_pel = pygame.transform.scale(supper_pel,(80,45))
        
        for row, line in enumerate(self.generator.maze):
            for col, cell in enumerate(line):
                x = col * cell_size
                y = row * cell_size
                # glow_color = (0, 80, 140)
                # core_color = (0, 220, 255)
                # glow_color, core_color = (100, 0, 150), (255, 0, 127)
                # glow_color, core_color = (110, 80, 50), (245, 235, 210)
                # glow_color, core_color = (60, 40, 20), (160, 130, 90)
                glow_color, core_color = (40, 28, 15), (120, 105, 90)
                if not (cell &1 and cell & 2 and cell & 4 and cell & 8):
                    if food is None:
                        self.screen.blit(self.normal_bel, (x+10, y+10))
                        food = [row.copy() for row in self.generator.maze]
                        food[0][0] = 20
                    elif [row,col] in super_pacgums: 
                        self.screen.blit(self.supper_pel,(x,y+10))
                        # if [row,col] == [0,self.size//2] and [row,col] in super_pacgums:
                        #     super_pacgums.remove([0,self.size//2])
                    elif self.generator.maze[row][col] == food[row][col]:
                        self.screen.blit(self.normal_bel, (x+10, y+10))
                # top
                if cell & 1:
                    # pygame.draw.line(self.screen, (100, 80, 120),(x, y),(x + cell_size, y), 3)
                    pygame.draw.line(self.screen, glow_color, (x, y), (x + cell_size, y), 5)
                    pygame.draw.line(self.screen, core_color, (x, y), (x + cell_size, y), 3)
                # right
                if cell & 2:
                    pygame.draw.line(self.screen, glow_color,(x + cell_size, y),(x + cell_size, y + cell_size), 5)
                    pygame.draw.line(self.screen, core_color,(x + cell_size, y),(x + cell_size, y + cell_size), 3)
                # bottom
                if cell & 4:
                    pygame.draw.line(self.screen, glow_color,(x, y + cell_size),(x + cell_size, y + cell_size), 5)
                    pygame.draw.line(self.screen, core_color,(x, y + cell_size),(x + cell_size, y + cell_size), 3)
                # left
                if cell & 8:
                    pygame.draw.line(self.screen, glow_color,(x, y),(x, y + cell_size), 5)
                    pygame.draw.line(self.screen, core_color,(x, y),(x, y + cell_size), 3)
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
                # nx, ny = current[0]-x, current[1]-y
                nx, ny = current[0]+x, current[1]+y
                move = [nx-current[0], ny-current[1]]
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
            return []
        curr = prevs
        while curr in queue:
            curr = queue[curr]
            res.append(list(curr))

        res.reverse()
        return res



class Ghosts:
    def __init__(self, size, size_cell,screen,directions,generator,len_path,speed_x,speed_y,function,p,paths,counter,time_live,ghost_name,speed,blinky_data=None,Flag_ability=True,counter_path=0,data={}):
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
        self.ghost_name = ghost_name
        self.blinky_data = blinky_data
        self.data = data
        self.Flag_ability = Flag_ability
        self.counter_path = counter_path
        self.speed = speed
        self.time_live = time_live
        self.is_dead = False


    def ft_position_ghost(self,position_pacman,position_ghost):
        paths = self.func.ft_find_paths_bfs(position_pacman,position_ghost)
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
        # if self.p >= len(self.paths)-1:
        #     self.p = 0
        if self.p < len(self.paths)-1:
            self.p += 1
      
        print("this also",self.paths[self.p][0],self.paths[self.p][1])
        next_node = self.paths[self.p]
        target_row, target_col = next_node[0], next_node[1]
        

        pos_row = target_row - ghost_y 
        pos_col = target_col - ghost_x
        # i thing i should remove this because it will not happen ? i forget why i do it 
        if pos_row > 1: 
            pos_row = 1
        if pos_row < -1:
            pos_row = -1
        if pos_col > 1:
            pos_col = 1
        if pos_col < -1:
            pos_col = -1
        print("it stop hereeeeeeeee")

        return ghost_x, ghost_y, [pos_row, pos_col]
  
    def ft_speed_ghost_blinky(self,ghost_x,ghost_y,pos,position_pacman):
        if pos is None:
            if self.ghost_name == "blinky" and self.Flag_ability:
                self.counter += 1
                if self.counter == 4:
                    position_ghosts,paths = self.ft_position_ghost(position_pacman,[ghost_y,ghost_x])
                    self.paths = paths
            ghost_x,ghost_y,pos = self.move_ghost(ghost_x,ghost_y)
            #add this one
            if pos == [0,0]:
                pos = None
        if pos is not None:
            if pos[0] != 0:
                self.speed_ghost_y += pos[0]* self.data["speed"]

            if pos[1] != 0:
                self.speed_ghost_x += pos[1]* self.data["speed"]
            
            if abs(self.speed_ghost_x) >= self.size_cell:
                ghost_x += pos[1]
                self.speed_ghost_x = 0
                pos = None

            elif abs(self.speed_ghost_y) >= self.size_cell:
                ghost_y += pos[0]
                self.speed_ghost_y = 0
                pos = None
           
        return self.speed_ghost_x,self.speed_ghost_y ,ghost_x, ghost_y,pos

    def ft_predict_target_pinky(self,ghost_x,ghost_y,pos,position_pacman,direction):
        new_positon = position_pacman.copy()
        if direction is not None:
            if direction[0] == 1:
                new_positon[0] += 4
            elif direction[1] == 1:
                new_positon[1] += 4
            elif direction[0]== -1:
                new_positon[0] -= 4
            elif direction[1] == -1:
                new_positon[1] -= 4
        if new_positon[0] < 0 or new_positon[0] > self.size[0]-1 or new_positon[1] < 0 or new_positon[1] > self.size[1]-1:
            new_positon = position_pacman.copy()

        
        if pos is None:
            self.counter += 1
            if self.counter == 4:
                n ,paths = self.ft_position_ghost(new_positon,[ghost_y,ghost_x])
                if not paths: 
                    n, paths = self.ft_position_ghost(position_pacman, [ghost_y, ghost_x])
                self.paths = paths
        
        speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_speed_ghost_blinky(ghost_x,ghost_y,pos,new_positon)
        
        return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos

    def ft_predict_target_inky(self,ghost_x,ghost_y,pos,position_pacman,direction):
        new_positon = position_pacman.copy()
        if direction is not None:
            if direction[0] == 1:
                new_positon[0] += 2
            elif direction[1] == 1:
                new_positon[1] += 2
            elif direction[0]== -1:
                new_positon[0] -= 2
            elif direction[1] == -1:
                new_positon[1] -= 2
        vector_y = new_positon[0] - self.blinky_data["ghost_y"]
        vector_x = new_positon[1] - self.blinky_data["ghost_x"]
        new_positon = [self.blinky_data["ghost_y"] + (vector_y * 2), self.blinky_data["ghost_x"] + (vector_x * 2)]

        # new_positon = [new_positon[0] - self.blinky_data["ghost_y"], new_positon[1] - self.blinky_data["ghost_x"]]
        
        if new_positon[0] < 0 or new_positon[0] > self.size[0]-1 or new_positon[1] < 0 or new_positon[1] > self.size[1]-1:
            new_positon = position_pacman.copy()
            if direction is not None:
                if direction[0] == 1:
                    new_positon[0] += 2
                elif direction[1] == 1:
                    new_positon[1] += 2
                elif direction[0]== -1:
                    new_positon[0] -= 2
                elif direction[1] == -1:
                    new_positon[1] -= 2
        
        if pos is None:
            self.counter += 1
            if self.counter == 4:
                n ,paths = self.ft_position_ghost(new_positon,[ghost_y,ghost_x])
                if not paths: 
                    n, paths = self.ft_position_ghost(position_pacman, [ghost_y, ghost_x])
                self.paths = paths
        
        speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_speed_ghost_blinky(ghost_x,ghost_y,pos,new_positon)
        
        return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos
    
    
    def ft_predict_target_clyde(self,ghost_x,ghost_y,pos,position_pacman,direction):
        new_positon = position_pacman.copy()
        if pos is None:
            self.counter += 1
            if self.counter == 4:
                n ,paths = self.ft_position_ghost(new_positon,[ghost_y,ghost_x])
                if not paths: 
                    n, paths = self.ft_position_ghost(position_pacman, [ghost_y, ghost_x])
                    
                if len(paths) >= 8:
                    self.paths = paths
                
                else:
                    n ,paths = self.ft_position_ghost([self.size[0]-1,0],[ghost_y,ghost_x])
                    self.paths = paths
                

        speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_speed_ghost_blinky(ghost_x,ghost_y,pos,new_positon)
        return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos

    def lose_ability_of_ghosts(self,ghost_x,ghost_y,pos,position_pacman,direction):
       
        if pos is None:
            if self.counter_path == 0:
                if self.ghost_name == "blinky":
                    target = [0,self.size[1]-1]
                    distance = abs(position_pacman[0] - target[0]) + abs(position_pacman[1] - target[1])
                    #i should to change it later for the maze if it small 
                    if distance < 5:
                        target = [self.size[0]-1,0]
                   
                elif self.ghost_name == "pinky":
                    target = [0,0]
                    distance = abs(position_pacman[0] - target[0]) + abs(position_pacman[1] - target[1])
                    if distance < 5:
                        target = [self.size[0]-1,self.size[1]-1]
                elif self.ghost_name == "inky":
                    target = [self.size[0] - 1, self.size[1] - 1]
                    distance = abs(position_pacman[0] - target[0]) + abs(position_pacman[1] - target[1])
                    if distance < 5:
                        target = [0,0]
                elif self.ghost_name == "clyde":
                    target = [self.size[0] - 1, 0]
                    distance = abs(position_pacman[0] - target[0]) + abs(position_pacman[1] - target[1])
                    if distance < 5:
                        target = [0,self.size[1]-1]
                self.p = 0
                n ,paths = self.ft_position_ghost(target,[ghost_y, ghost_x])
                if not paths:
                    n, paths = self.ft_position_ghost([0,0],[ghost_y, ghost_x])
                self.paths = paths

            self.counter_path +=1
            if self.counter_path >=  4:
                self.counter_path = 0
        
    def ft_speed_ghost(self,ghost_x,ghost_y,pos,position_pacman,pac_man_direction,star_time):
        if star_time is not None:
            if time.time() - star_time >= 20: 
                self.Flag_ability = True
                star_time = None
                self.data["speed"] = 1
                self.paths = []
        if self.is_dead:
            if time.time() - self.time_live < 10:
                return None
            else:
                self.is_dead = False
        if not self.Flag_ability:
            self.lose_ability_of_ghosts(ghost_x,ghost_y,pos,position_pacman,pac_man_direction)
            speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_speed_ghost_blinky(ghost_x,ghost_y,pos,position_pacman)
            return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos
        if self.ghost_name == "blinky":
            speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_speed_ghost_blinky(ghost_x,ghost_y,pos,position_pacman)
            return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos

        elif self.ghost_name == "pinky":
            speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_predict_target_pinky(ghost_x,ghost_y,pos,position_pacman,pac_man_direction)
            return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos

        elif self.ghost_name == "inky":
            speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_predict_target_inky(ghost_x,ghost_y,pos,position_pacman,pac_man_direction)
            return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos

        elif self.ghost_name == "clyde":
            speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos = self.ft_predict_target_clyde(ghost_x,ghost_y,pos,position_pacman,pac_man_direction)
            return speed_ghost_x,speed_ghost_y ,ghost_x, ghost_y,pos




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
        background = (15, 15, 20)
        speed_ghostx=0
        speed_ghosty=0
        size=(14, 14)
        position_pacman = [0, size[0]//2]
        
        move = False
        close = True
        paths = []
        generator = MazeGenerator(
                size,
                perfect=False,
                entry_cell=(0, 0),
                exit_cell=(-1, -1),
                seed=0
            )
   

        directions_wall = [[1,0],[-1,0],[0,-1],[0,1]]

        



        # screen = pygame.display.set_mode((size[1]*50,size[0]*50))
        screen = pygame.display.set_mode((size[1]*50,(size[0]*50)+70))
        width, height = screen.get_size()
        size_screen = [width,height] 
        height -= 70
        size_cell = min(width//size[1],height//size[0])
        speed_x = 0
        speed_y = 0
        counter = 0
        Flag_ability = True
        data = {"speed": 1}
        time_live = time.time()
        # normal_pel,(45,25
        normal_pel = pygame.image.load("image/normal_bel.png")
        normal_pel = pygame.transform.scale(normal_pel,(35, 20))

        supper_pel = pygame.image.load("image/supper_bel.png")
        supper_pel = pygame.transform.scale(supper_pel,(45,25))

        
        

        render = Player(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,0,normal_pel,supper_pel)
        blinky = Ghosts(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,render,0,paths,counter,time_live,"blinky" , None,Flag_ability,data)
        pinky = Ghosts(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,render,0,paths,counter,time_live,"pinky",None,Flag_ability,data)
        inky = Ghosts(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,render,0,paths,counter,time_live,"inky",None,Flag_ability,data)
        clyde = Ghosts(size, size_cell, screen,directions_wall,generator,0,speed_x,speed_y,render,0,paths,counter,time_live,"clyde",None,Flag_ability,data)

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
        score = 0
        font = pygame.font.SysFont("Arial", 20)
        score_surface = font.render(f"Score: {score}", True, (245, 245, 220))
        # => change the coordonation of the ghost later or atleast check there coordination before give theme
        # image = pygame.transform.rotate(pacman_image, 0)
        
        
        pac_man_right = pygame.image.load("image/right_pacman.png")
        pac_man_left = pygame.image.load("image/left_pacman.png")
        pac_man_up = pygame.image.load("image/up_pacman.png")
        pac_man_down = pygame.image.load("image/down_pacman.png")
        # pac_close = pygame.image.load("image/close.png")

        pac_man_right = pygame.transform.scale(pac_man_right,(70,45))
        pac_man_left = pygame.transform.scale(pac_man_left,(70,45))
        pac_man_up = pygame.transform.scale(pac_man_up,(70,45))
        pac_man_down = pygame.transform.scale(pac_man_down,(70,45))

        # leftclose_pacman
        close_right = pygame.image.load("image/rightclose_pac.png")
        close_left = pygame.image.load("image/leftclose_pacman.png")
        close_up = pygame.image.load("image/upclose_pacman.png")
        close_down = pygame.image.load("image/downclose_pacman.png")
        #ghost weak
        ghost_weak = pygame.image.load("image/weakghost.png")
        ghost_weak = pygame.transform.scale(ghost_weak,(80,45))

        close_right = pygame.transform.scale(close_right,(70,45))
        close_left = pygame.transform.scale(close_left,(70,45))
        close_up = pygame.transform.scale(close_up,(70,45))
        close_down = pygame.transform.scale(close_down,(70,45))


        Ghost_red = pygame.image.load("image/ghost_red.png")
        ghost_red = pygame.transform.scale(Ghost_red,(80,45))

        ghost_pink = pygame.image.load("image/ghost_pink.png")
        ghost_pink = pygame.transform.scale(ghost_pink,(80,45))

        ghost_blue = pygame.image.load("image/ghost_blue.png")
        ghost_blue = pygame.transform.scale(ghost_blue,(80,45))

        ghost_yellow = pygame.image.load("image/ghost_yellow.png")
        ghost_yellow = pygame.transform.scale(ghost_yellow,(80,45))

        heart_image = pygame.image.load("image/heart.png")
        heart_image = pygame.transform.scale(heart_image,(45,45))

        # pac_man_close = pygame.transform.scale(pac_close,(65,40))
        
        # normal_pel = pygame.image.load("image/normal_bel.png")
        # normal_pel = pygame.transform.scale(normal_pel,(80,45))

        # supper_pel = pygame.image.load("image/supper_bel.png")
        # supper_pel = pygame.transform.scale(supper_pel,(80,45))
        
        ghosts_list = [
            {"ghost": blinky, "ghost_x": 0, "ghost_y": 0, "pos": None, "speed_x": 0, "speed_y": 0,"draw":"B","time":None,"speed":1,"cheat": False,"image":ghost_red},
            {"ghost": pinky,  "ghost_x": 0, "ghost_y": size[1]-1, "pos": None, "speed_x": 0, "speed_y": 0,"draw":"P","time":None,"speed":1,"cheat": False,"image":ghost_pink},
            {"ghost": inky,  "ghost_x": size[0]-1, "ghost_y": 0, "pos": None, "speed_x": 0, "speed_y": 0,"draw":"I","time":None,"speed":1,"cheat": False,"image":ghost_blue},
            {"ghost": clyde,  "ghost_x": size[0]-1, "ghost_y": size[1]-1, "pos": None, "speed_x": 0, "speed_y": 0,"draw":"C","time":None,"speed":1,"cheat": False,"image":ghost_yellow} 
        ]
        info_second_try = ghosts_list.copy()
        speed_pac_man = 3
        #here to test cheat mode 
       
        # for g in ghosts_list:
        #     g["cheat"] = True
        #     g["time"] = time.time()
        for g in ghosts_list:
            position_ghosts,paths = blinky.ft_position_ghost(position_pacman,[g["ghost_y"],g["ghost_x"]])
            g["ghost"].paths = paths
  
        inky.blinky_data = ghosts_list[0]
    
        for g in ghosts_list:
            g["ghost"].data = data
        x = 0
        y = 0
        food = None
        flag_picture = -1
        counter_heart = 0 
        clock = pygame.time.Clock()
        list_heart = [60,100,140]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key in directions:
                        pending_pos = directions[event.key]
                    if event.key == pygame.K_SPACE:
                        show_path = True
            # if pending_pos is not None and step_x == 0 and step_y == 0:
            #         #here i do pos that for reserve my previous value of direction  
            #         pos = pending_pos
            #         pending_pos = None
            if pending_pos is not None and step_x == 0 and step_y == 0:
                row = position_pacman[0]
                col = position_pacman[1]
                if render.ft_check_walls(pending_pos, row, col):
                    pos = pending_pos
                    pending_pos = None
                
            
            
            if pos:
                row = position_pacman[0]
                col = position_pacman[1]
                if render.ft_check_walls(pos,row,col):
                    step_x += pos[1] * speed_pac_man
                    step_y += pos[0] * speed_pac_man
                    if abs(step_x) >= size_cell:
                        flag_picture *= -1
                        step_x = 0
                        position_pacman[1] += pos[1]
                        if food:
                            score += 5
                            food[row][position_pacman[1]] = 20
                            if [row,position_pacman[1]] in super_pacgums:
                                score += 95
                                super_pacgums.remove([row,position_pacman[1]])
                                for g in ghosts_list:
                                    g["ghost"].Flag_ability = False
                                    g["time"]  = time.time()
                                    g["speed"] = 0.5
                    if abs(step_y) >= size_cell:
                        flag_picture *= -1
                        step_y = 0
                        position_pacman[0] += pos[0]
                        if food:
                            score += 5
                            food[position_pacman[0]][col] = 20
                            if [position_pacman[0],col] in super_pacgums:
                                super_pacgums.remove([position_pacman[0],col])
                                score += 95
                                for g in ghosts_list:
                                    g["ghost"].Flag_ability = False
                                    g["time"] = time.time()
                                    g["speed"] = 0.5

            x = (position_pacman[1] * size_cell) + step_x
            y = (position_pacman[0] * size_cell) + step_y
            screen.fill(background)
            food,super_pacgums = render.display(pos,food,super_pacgums)

            for g in ghosts_list:
                result = g["ghost"].ft_speed_ghost(g["ghost_x"],g["ghost_y"],g["pos"],position_pacman,pos,g["time"])
                if result is None:
                    continue 
                g["speed_x"], g["speed_y"], g["ghost_x"], g["ghost_y"], g["pos"] = result

                ghost = font.render(g["draw"], True, (255, 255, 255))

                difx_subtraction = abs(((g["ghost_x"]*size_cell)+g["speed_x"]-10) - (x-10))
                dify_subtraction = abs(((g["ghost_y"]*size_cell)+g["speed_y"]+2) - (y+2))
                if g["cheat"]:
                    screen.blit(g["image"],((g["ghost_x"]*size_cell)+g["speed_x"]-10,(g["ghost_y"]*size_cell)+g["speed_y"]+2))
                    speed_pac_man = 5
                if difx_subtraction <= size_cell//2 and dify_subtraction <= size_cell//2  and not g["ghost"].Flag_ability:
                    if time.time() - g["time"] >= 20:
                        screen.blit(g["image"],((g["ghost_x"]*size_cell)+g["speed_x"]-10,(g["ghost_y"]*size_cell)+g["speed_y"]+2))
                    else:
                        if g["draw"] == "B":
                            g["ghost_x"], g["ghost_y"] = 0, 0
                        elif g["draw"] == "P":
                            g["ghost_x"], g["ghost_y"] = 0, size[1]-1
                        elif g["draw"] == "I":
                            g["ghost_x"], g["ghost_y"] = size[0]-1, 0
                        elif g["draw"] == "C":
                            g["ghost_x"], g["ghost_y"] = size[0]-1, size[1]-1
                        g["speed_x"] = 0
                        g["speed_y"] = 0
                        g["pos"] = None
                        g["speed"]= 1
                        g["ghost"].paths = []
                        g["ghost"].p = 0
                        g["ghost"].Flag_ability = True
                        g["ghost"].time_live = time.time()
                        g["ghost"].is_dead = True
                elif difx_subtraction <= size_cell//2 and dify_subtraction <= size_cell//2 and g["ghost"].Flag_ability:
                    if len(list_heart) > 0:
                        list_heart.pop(-1)
                        position_pacman = [0, size[0]//2]
                        step_x = 0
                        step_y = 0
                        pos = None
                        pending_pos = None
                        
                        ghosts_list = info_second_try.copy()
                        ghosts_list[0]["ghost_x"], ghosts_list[0]["ghost_y"] = 0, 0
                        ghosts_list[1]["ghost_x"], ghosts_list[1]["ghost_y"] = 0, size[1]-1
                        ghosts_list[2]["ghost_x"], ghosts_list[2]["ghost_y"] = size[0]-1, 0
                        ghosts_list[3]["ghost_x"], ghosts_list[3]["ghost_y"] = size[0]-1, size[1]-1

                        for item in ghosts_list:
                            item["ghost_x"] = item["ghost_x"]
                            item["ghost_y"] = item["ghost_y"]
                            item["pos"] = None
                            item["speed_x"] = 0
                            item["speed_y"] = 0
                            item["ghost"].speed_ghost_x = 0
                            item["ghost"].speed_ghost_y = 0
                            item["ghost"].p = 0
                            item["ghost"].Flag_ability = True
                            item["ghost"].is_dead = False
                            position_ghosts, paths = blinky.ft_position_ghost(position_pacman, [item["ghost_y"], item["ghost_x"]])
                            item["ghost"].paths = paths
                            
                        break
                    else:
                        # print("it do this ===========")
                        sys.exit()

                elif g["ghost"].Flag_ability:
                    screen.blit(g["image"],((g["ghost_x"]*size_cell)+g["speed_x"]-10,(g["ghost_y"]*size_cell)+g["speed_y"]+2))
                else:
                    screen.blit(ghost_weak,((g["ghost_x"]*size_cell)+g["speed_x"]-10,(g["ghost_y"]*size_cell)+g["speed_y"]+2))


                p = g["ghost"].ft_render_paths_debug(g["ghost"].paths,show_path,p)
                    
            # screen.blit(heart_image, (size_screen[0] - 60, size_screen[1] - 60))
            # screen.blit(heart_image, (size_screen[0] - 100, size_screen[1] - 60))
            # screen.blit(heart_image, (size_screen[0] - 140, size_screen[1] - 60))

            score_surface = font.render(f"Score: {score}", True, (245, 245, 220))
            screen.blit(score_surface, (10, size_screen[1] - 50))
            
            
            for n in list_heart:
                screen.blit(heart_image, (size_screen[0] - n, size_screen[1] - 60))
            if pos == [0,1]:
                if flag_picture == -1:
                    screen.blit(pac_man_right, (x-10, y+2))
                else:
                    screen.blit(close_right, (x-10, y+2))

            elif pos == [0,-1]:
                if flag_picture == -1:
                    screen.blit(pac_man_left, (x-10, y+2))
                else:
                    screen.blit(close_left, (x-10, y+2))
            elif pos == [1,0]:
                if flag_picture == -1:
                    screen.blit(pac_man_down,(x-10, y+2))
                else:
                    screen.blit(close_down, (x-10, y+2))
            elif pos == [-1,0]:
                if flag_picture == -1:
                    screen.blit(pac_man_up,(x-10, y+2))
                else:
                    screen.blit(close_up, (x-10, y+2))
            else:
                screen.blit(pac_man_right, (x-10, y+2))
            
            
            pygame.time.get_ticks()

            show_path = False
            pygame.display.flip()
            
            clock.tick(60)

        pygame.quit()   
        sys.exit()

if __name__ == "__main__":
    Display().run()