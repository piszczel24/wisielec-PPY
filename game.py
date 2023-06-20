import pygame

WIDTH = 800
HEIGHT = 600
FPS = 60
BG_COLOR = (9, 161, 139)


class Game:
    def __init__(self):
        pygame.init()

        # Zmienne globalne
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Comic sans MS", 50)
        self.is_running = True

        # Szkielet aplikacji
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOR)
        pygame.display.set_caption("Wisielec")
        pygame.display.set_icon(pygame.image.load("img/icon.png"))

    def check_input(self):
        # Pętla sprawdzająca wciśnięte przyciski
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())

    def run(self):
        # Gra właściwa
        while self.is_running:
            self.check_input()

            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


game = Game()
game.run()
