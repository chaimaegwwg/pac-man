from mazegenerator import MazeGenerator
import pygame, sys

def display(screen):
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    cell_size = 40
    generator = MazeGenerator(
        size=(15, 15),
        perfect=False,
        entry_cell=(0, 0),
        exit_cell=(-1, -1),
        seed=0
    )
    print(generator.maze)
    for row, line in enumerate(generator.maze):
        for col, cell in enumerate(line):
            x = col * cell_size
            y = row * cell_size

            # Top
            if cell & 1:
                pygame.draw.line(
                    screen, (0, 0, 0),
                    (x, y),
                    (x + cell_size, y),
                    2
                )

            # Right
            if cell & 2:
                pygame.draw.line(
                    screen, (0, 0, 0),
                    (x + cell_size, y),
                    (x + cell_size, y + cell_size),
                    2
                )

            # Bottom
            if cell & 4:
                pygame.draw.line(
                    screen, (0, 0, 0),
                    (x, y + cell_size),
                    (x + cell_size, y + cell_size),
                    2
                )

            # Left
            if cell & 8:
                pygame.draw.line(
                    screen, (0, 0, 0),
                    (x, y),
                    (x, y + cell_size),
                    2
                )
        
            

screen = pygame.display.set_mode((800,800))
white = (255, 255, 255)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(white)
    display(screen)
    pygame.display.flip()

pygame.quit()   
sys.exit()
# print(generator.maze)