import pygame


def draw_menu(screen):
    screen.fill((0, 0, 0))

    font = pygame.font.Font(None, 80)

    title = font.render("PACMAN Menu", True, (255, 255, 0))

    screen.blit(title, (300, 100))