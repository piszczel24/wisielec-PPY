import pygame
from player import Player
from button import Button

WIDTH = 1600
HEIGHT = 900
FPS = 60
BG_COLOR = (9, 161, 139)
ALPHABET = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŻŹ"


def find_indexes(letter, text):
    indexes = []
    for i in range(len(text)):
        if text[i] == letter:
            indexes.append(i)
    return indexes


class Game:
    def __init__(self, player1: Player, player2: Player) -> None:
        pygame.init()

        # Zmienne globalne
        self.clock = pygame.time.Clock()
        self.player_font = pygame.font.SysFont("Comic sans MS", 50)
        self.word_font = pygame.font.SysFont("Comic sans MS", 40)
        self.is_running = True
        self.images = [pygame.image.load(f"img/{i}.png") for i in range(11)]

        # Szkielet aplikacji
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Wisielec")
        pygame.display.set_icon(pygame.image.load("img/icon.png"))

        # Zeminne dot. bierzącej gry
        self.current_step = 10
        self.players = (player1, player2)
        self.current_player = self.players[0]
        self.category = "Literaturoznawstwo"
        self.word = "Anastazja".upper()
        self.letters_remaining = len(self.word)
        self.guessed_word_list = ["_" for _ in range(self.letters_remaining)]
        self.guessed_word = self.get_guessed_word()

        # Elementy na ekranie
        self.hangman_surface = self.images[0]
        self.hangman_rect = self.hangman_surface.get_rect(midleft=(0, 300))

        self.current_player_surface = self.player_font.render(f"Tura gracza: {self.current_player.nickname}", True,
                                                              "black")
        self.current_player_rect = self.current_player_surface.get_rect(midtop=(1100, 10))

        self.category_surface = self.word_font.render(f"Kategoria: {self.category}", True, "black")
        self.category_rect = self.category_surface.get_rect(topleft=(40, 630))

        self.guessed_word_surface = self.word_font.render(self.guessed_word, True, "black")
        self.guessed_word_rect = self.guessed_word_surface.get_rect(topleft=(40, 750))

        self.buttons = []
        self.load_buttons()

    def run(self) -> None:
        while self.is_running:
            self.check_input()
            self.draw_content()
            self.clock.tick(FPS)

        pygame.quit()

    def check_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.collidepoint(event.pos):
                        button.is_visible = False
                        self.check_letter(button)

    def check_letter(self, button: Button) -> None:
        if button.letter in self.word:
            indexes = find_indexes(button.letter, self.word)
            for index in indexes:
                self.guessed_word_list[index] = button.letter
                self.guessed_word = self.get_guessed_word()
                self.letters_remaining -= 1

    def draw_content(self):
        self.screen.fill(BG_COLOR)
        self.hangman_surface = self.images[self.current_step]
        self.screen.blit(self.hangman_surface, self.hangman_rect)
        self.screen.blit(self.current_player_surface, self.current_player_rect)
        self.screen.blit(self.category_surface, self.category_rect)

        self.guessed_word_surface = self.word_font.render(self.guessed_word, True, "black")
        self.screen.blit(self.guessed_word_surface, self.guessed_word_rect)
        for button in self.buttons:
            button.draw()
        pygame.display.update()

    def load_buttons(self):
        horizontal_offset = 200
        vertical_offset = 100
        alphabet_letter_number = 0
        for i in range(8):
            for j in range(4):
                self.buttons.append(Button(800 + (j * horizontal_offset), 100 + (i * vertical_offset), 50, 50,
                                           ALPHABET[alphabet_letter_number], self.screen))
                alphabet_letter_number += 1

    def get_guessed_word(self) -> str:
        result = ""
        for letter in self.guessed_word_list:
            result += letter
            result += " "
        return result


player1 = Player(1, "A")
player2 = Player(2, "B")

game = Game(player1, player2)
game.run()
