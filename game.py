import pygame
from player import Player

WIDTH = 1600
HEIGHT = 900
FPS = 60
BG_COLOR = (9, 161, 139)


class Game:
    def __init__(self, player1: Player, player2: Player):
        pygame.init()

        # Zmienne globalne
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Comic sans MS", 50)
        self.is_running = True
        self.images = []
        self.load_images()

        # Szkielet aplikacji
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOR)
        pygame.display.set_caption("Wisielec")
        pygame.display.set_icon(pygame.image.load("img/icon.png"))

        # Zeminne dot. bierzącej gry
        self.current_step = 10  # Obecny stan wisielca 0-10
        self.players = (player1, player2)
        self.cuurent_player = self.players[0]
        self.category = "Literaturoznawstwo"

        # Elementy na ekranie
        self.hangman_surface = self.images[0]
        self.hangman_rect = self.hangman_surface.get_rect(midleft=(0, 300))  # Właściwy wisielec

        self.current_player_surface = self.font.render(f"Tura gracza: {self.cuurent_player.nickname}", True, "black")
        self.current_player_rect = self.current_player_surface.get_rect(midtop=(1100, 10))  # Czyja tura

        self.category_surface = self.font.render(f"Kategoria: {self.category}", True, "black")
        self.category_rect = self.category_surface.get_rect(topleft=(10, 630))

    def run(self):
        # Gra właściwa
        while self.is_running:
            self.hangman_surface = self.images[self.current_step]
            self.screen.blit(self.hangman_surface, self.hangman_rect)
            self.screen.blit(self.current_player_surface, self.current_player_rect)
            self.screen.blit(self.category_surface, self.category_rect)

            self.check_input()
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()

    def check_input(self):
        # Pętla sprawdzająca wciśnięte przyciski
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def load_images(self):
        for i in range(0, 11):
            self.images.append(pygame.image.load(f"img/{i}.png"))


player1 = Player(1, "A")
player2 = Player(2, "B")

game = Game(player1, player2)
game.run()
