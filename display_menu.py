import pygame


def draw_menu(screen):
    screen.fill((0, 0, 0))

    title_font = pygame.font.Font(None, 80)
    option_font = pygame.font.Font(None, 45)

    title = title_font.render("PACMAN Menu", True, (255, 255, 0))

    screen.blit(title, (300, 100))

    options = ["START GAME", "OPTIONS", "QUIT"]

    for i, option in enumerate(options):
        text = option_font.render(option, True, (255, 255, 255))
        screen.blit(text, (320, 250 + i * 60))