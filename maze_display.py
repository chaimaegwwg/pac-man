from mazegenerator import MazeGenerator
import pygame, sys

# top = 1
# right = 2
# bottom = 4
# left = 8
def display(screen,generator,pos):
    pygame.init()
    black = (0, 0, 0)
    width, height = screen.get_size()
    #suppose the arr has 15 col and row that why we will see if it change or not 
    cell_size = min(width//15,height//15)
    for row, line in enumerate(generator.maze):
        for col, cell in enumerate(line):
            x = col * cell_size
            y = row * cell_size
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

            
#from now i will like just test that and i will start from 0,0 after that i will change it to the middle
def ft_check_walls(pos, row , col,generator):
    cell = generator.maze[row][col]
    if pos[0] == 1:
        if cell & 2:
            return False
    if pos[0] == -1:
        if cell & 8:
            return False
    if pos[1] == 1:
        if cell & 4:
            return False
    if pos[1] == -1:
        if cell & 1:
            return False
    return True




screen = pygame.display.set_mode((800,800))
size_cell = 800 // 15
start_to = 5
# pacman = pygame.image.load("pacman_up.png")
# screen.blit(pacman, (x, y))
pygame.init()
#this is for not each time i will press the key

character_pacman = "@"
position_pacman = [0,0]
checker_x = 0
checker_y = 0
background = (15, 15, 20)
generator = MazeGenerator(
        size=(15, 15),
        perfect=False,
        entry_cell=(0, 0),
        exit_cell=(-1, -1),
        seed=0
    )
font = pygame.font.Font(None, 40)
running = True
pos= None
directions = { 
    pygame.K_RIGHT :[1,0], 
    pygame.K_LEFT: [-1,0], 
    pygame.K_UP: [0,-1], 
    pygame.K_DOWN:[0,1] 
}
step_x = 0
step_y = 0
x=0
y=0
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key in directions:
                pos = directions[event.key]
    if pos:
        row = position_pacman[0]
        col = position_pacman[1]
        if ft_check_walls(pos,row,col,generator):
            step_x += pos[0] * 5.3
            step_y += pos[1] * 5.3
            if abs(step_x) >= size_cell:
                step_x = 0 
                position_pacman[1] += pos[0]
            if abs(step_y) >= size_cell:
                step_y = 0
                position_pacman[0] += pos[1]
        x = (position_pacman[1] * size_cell) + step_x
        y = (position_pacman[0] * size_cell) + step_y

        x += (size_cell - pacman.get_width()) // 2
        y += (size_cell - pacman.get_height()) // 2
    screen.fill(background)
    display(screen,generator,pos)
    pacman = font.render("@", True, (255, 255, 0))
    screen.blit(pacman, (x, y))
    pygame.display.flip()
    clock.tick(30)


pygame.quit()   
sys.exit()