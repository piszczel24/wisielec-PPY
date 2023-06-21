import pygame
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base

from button import Button
from playerdto import PlayerDto
from db_initialize import Player, Category, Word

WIDTH = 1600
HEIGHT = 900
FPS = 60
BG_COLOR = (9, 161, 139)
ALPHABET = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŻŹ"

Base = declarative_base()

engine = create_engine("postgresql://pycharm:pycharm@localhost:5432/postgres", echo=True)
Session = sessionmaker(bind=engine)


def find_indexes(letter: str, text: str) -> list[int]:
    indexes = []
    for i in range(len(text)):
        if text[i] == letter:
            indexes.append(i)
    return indexes


class Game:
    def __init__(self, player1: PlayerDto, player2: PlayerDto) -> None:
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
        self.current_step = 0
        self.players = [player1, player2]
        self.current_player = 0

        self.session = Session()
        self.category, self.word = self.pick_category_and_word()
        self.category_string = self.category.name
        self.word_string = self.word.word.upper()
        self.session.commit()

        self.letters_remaining = len(self.word_string)
        self.guessed_word_list = ["_" for _ in range(self.letters_remaining)]
        self.guessed_word = self.get_guessed_word()
        self.winner = None

        # Elementy na ekranie
        self.hangman_surface = self.images[0]
        self.hangman_rect = self.hangman_surface.get_rect(midleft=(0, 300))

        self.current_player_surface = self.player_font.render(
            f"Tura gracza: {self.players[self.current_player].nickname}", True, "black")
        self.current_player_rect = self.current_player_surface.get_rect(midtop=(1100, 10))

        self.category_surface = self.word_font.render(f"Kategoria: {self.category_string}", True, "black")
        self.category_rect = self.category_surface.get_rect(topleft=(40, 630))

        self.guessed_word_surface = self.word_font.render(self.guessed_word, True, "black")
        self.guessed_word_rect = self.guessed_word_surface.get_rect(topleft=(40, 750))

        self.buttons = []
        self.load_buttons()

    def run(self) -> None:
        while self.is_running:
            self.check_input()
            self.draw_content()
            self.check_finish()
            self.clock.tick(FPS)

        pygame.quit()

    def check_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.collidepoint(event.pos):
                        button.is_visible = False

                        self.check_letter(button)
                        self.change_player()

    def check_letter(self, button: Button) -> None:
        if button.letter in self.word_string:
            indexes = find_indexes(button.letter, self.word_string)
            for index in indexes:
                self.guessed_word_list[index] = button.letter
                self.guessed_word = self.get_guessed_word()
                self.letters_remaining -= 1
        elif self.current_step <= 11:
            self.current_step += 1

    # def check_finish(self):

    def draw_content(self) -> None:
        self.screen.fill(BG_COLOR)
        self.hangman_surface = self.images[self.current_step]
        self.screen.blit(self.hangman_surface, self.hangman_rect)
        self.current_player_surface = self.player_font.render(
            f"Tura gracza: {self.players[self.current_player].nickname}", True, "black")
        self.screen.blit(self.current_player_surface, self.current_player_rect)
        self.screen.blit(self.category_surface, self.category_rect)

        self.guessed_word_surface = self.word_font.render(self.guessed_word, True, "black")
        self.screen.blit(self.guessed_word_surface, self.guessed_word_rect)
        for button in self.buttons:
            button.draw()
        pygame.display.update()

    def load_buttons(self) -> None:
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

    def check_finish(self) -> None:
        if self.current_step == 10:
            self.is_running = False
            self.winner = self.players[self.current_player]
            print(f"WINNER: {self.winner.nickname}")
        elif self.letters_remaining <= 0:
            self.change_player()
            self.is_running = False
            self.winner = self.players[self.current_player]
            print(f"WINNER: {self.winner.nickname}")

    def change_player(self) -> None:
        if self.current_player == 0:
            self.current_player = 1
        elif self.current_player == 1:
            self.current_player = 0

    def pick_category_and_word(self) -> Category:
        category: Category = self.session.query(Category).order_by(func.random()).first()
        word = self.session.query(Word).filter_by(category_id=category.id).order_by(func.random()).first()
        return category, word
