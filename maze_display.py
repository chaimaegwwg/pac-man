from mazegenerator import MazeGenerator
import pygame, sys

def display(screen):
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    cell_size = 20
    generator = MazeGenerator(
        size=(15, 15),
        perfect=False,
        entry_cell=(0, 0),
        exit_cell=(-1, -1),
        seed=0
    )
    for index_x, x in enumerate(generator.maze):
        for index_y, y in enumerate(x):
            if index_x % 2 == 0:
                print("----",end=" ")
            if index_x % 2!= 0:
                print("|",end="   ")
        print()
        
            # pygame.draw.rect(screen, black, (x,y,10,10))



    #         pygame.draw.line(sc, pygame.Color('darkgreen'), (x, y), (x + tile, y), self.thickness)


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
# print(generator.maze)