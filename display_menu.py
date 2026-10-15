import pygame

SCREEN_WIDTH = 14 * 50
SCREEN_HEIGHT = 14 * 50
FPS = 60


class Menu:
    def __init__(self):
        self.bg = pygame.image.load('img.png')
        self.option_font = pygame.font.Font('WowDino-G33vP.ttf', 60)
        self.title_font1 = pygame.font.Font('PAC-FONT.TTF', 35)
        self.title_font2 = pygame.font.Font('PAC-FONT.TTF', 60)


    def draw_centred_text(
        self, screen, text, font, y, text_color=(255, 255, 255)
    ):
        rendered_text = font.render(text, True, text_color)
        rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, y))
        screen.blit(rendered_text, rect)
        # print(rect)


    def draw_button(self, screen):
        button = pygame.Rect(170, 475, 355, 58)

        pygame.draw.rect(screen, [180, 21, 0], button, 0, 30)



    def draw_menu(self, screen):
        screen.fill((0, 0, 0))
        # bg = pygame.image.load('img.png')
        screen.blit(self.bg, (0, 0))
        # print(pygame.font.get_fonts())
        # option_font = pygame.font.SysFont("lato", 60)
        # title_font1 = pygame.font.Font('PAC-FONT.TTF', 35)
        # title_font2 = pygame.font.Font('PAC-FONT.TTF', 60)

        # draw_centred_text(screen, "hello, center", test_font, 100)
        # self.draw_button(screen)

        self.draw_centred_text(
            screen, "I WANNA BE A", self.title_font1, 100, (255, 255, 0)
        )
        self.draw_centred_text(
            screen, "pac- man", self.title_font2, 180, (255, 255, 0)
        )
        self.draw_centred_text(screen, "press to start", self.option_font, 500, (180, 21, 0))


        # options = ["START GAME", "EXIT"]

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
    menu = Menu()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
 
        menu.draw_menu(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
