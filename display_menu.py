import pygame


def draw_menu(screen):
    screen.fill((0, 0, 0))

    title_font = pygame.font.Font(None, 80)
    option_font = pygame.font.Font(None, 45)

    title = title_font.render("PACMAN Menu", True, (255, 255, 0))

    screen.blit(title, (200, 100))

    options = ["START GAME", "OPTIONS", "QUIT"]

    for i, option in enumerate(options):
        text = option_font.render(option, True, (255, 255, 255))
        screen.blit(text, (200, 250 + i * 60))

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Pacman Menu Test")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_menu(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()


