import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60


def draw_centred_text(
    screen, text, font, y, text_color=(255, 255, 255), bg_color=(0, 0, 0)
):
    rendred_text = font.render(text, True, text_color, bg_color)
    rect = rendred_text.get_rect(center=(SCREEN_WIDTH // 2, y // 2))
    screen.blit(rendred_text, rect)
    # print(rect)


def draw_menu(screen):
    screen.fill((0, 0, 0))

    # print(pygame.font.get_fonts())
    option_font = pygame.font.SysFont("lato", 60)
    title_font = pygame.font.Font('PacmanicRegular-vPyE.ttf', 80)

    # draw_centred_text(screen, "hello, center", test_font, 100)

    draw_centred_text(
        screen, "PACMAN Game", title_font, 400, (255, 255, 0)
    )

    draw_centred_text(screen, "press to start", option_font, 1000)
    # title = title_font.render("PACMAN Menu", True, (255, 255, 0))

    # screen.blit(title, (200, 100))

    options = ["START GAME", "OPTIONS", "QUIT"]

    # for i, option in enumerate(options):
    #     draw_centred_text(screen, option, option_font, 500 + i * 100)
        # text = option_font.render(option, True, (255, 255, 255))
        # screen.blit(text, (200, 250 + i * 60))


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pac-man")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        draw_menu(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
