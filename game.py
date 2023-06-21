import pygame
from player import Player
from button import Button

WIDTH = 1600
HEIGHT = 900
FPS = 60
BG_COLOR = (9, 161, 139)


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        pygame.init()

        self.hangman_rect_vis = True

        # Zmienne globalne
        self.clock = pygame.time.Clock()
        self.player_font = pygame.font.SysFont("Comic sans MS", 50)
        self.category_font = pygame.font.SysFont("Comic sans MS", 40)
        self.is_running = True
        self.images = [pygame.image.load(f"img/{i}.png") for i in range(11)]

        # Szkielet aplikacji
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(BG_COLOR)
        pygame.display.set_caption("Wisielec")
        pygame.display.set_icon(pygame.image.load("img/icon.png"))

        # Zeminne dot. bierzącej gry
        self.current_step = 10  # Obecny stan wisielca 0-10
        self.players = (player1, player2)
        self.current_player = self.players[0]
        self.category = "Literaturoznawstwo"
        self.word = "dzięcielina".upper()

        # Elementy na ekranie
        self.hangman_surface = self.images[0]
        self.hangman_rect = self.hangman_surface.get_rect(midleft=(0, 300))  # Właściwy wisielec

        self.current_player_surface = self.player_font.render(f"Tura gracza: {self.current_player.nickname}", True,
                                                              "black")
        self.current_player_rect = self.current_player_surface.get_rect(
            midtop=(1100, 10))  # Napis pokazujący, kogo jest tura

        self.category_surface = self.category_font.render(f"Kategoria: {self.category}", True, "black")
        self.category_rect = self.category_surface.get_rect(topleft=(40, 630))

        self.button = Button(800, 100, 50, 50, "A", self.screen)

    def run(self) -> None:
        # Gra właściwa
        while self.is_running:
            self.check_input()
            self.draw_countent()
            self.clock.tick(FPS)

        pygame.quit()

    def check_input(self):
        # Pętla sprawdzająca wciśnięte przyciski
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.button.is_visible:
                if self.hangman_rect.collidepoint(event.pos):
                    self.hangman_rect_vis = False

    def draw_countent(self):

        if self.hangman_rect_vis:
            self.hangman_surface = self.images[self.current_step]
            self.screen.blit(self.hangman_surface, self.hangman_rect)
        self.screen.blit(self.current_player_surface, self.current_player_rect)
        self.screen.blit(self.category_surface, self.category_rect)
        print(self.hangman_rect_vis)
        # self.button.draw()
        pygame.display.update()


player1 = Player(1, "A")
player2 = Player(2, "B")

game = Game(player1, player2)
game.run()
