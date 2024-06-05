"""Moduł zawiera klasę z grą, w tym całą jej mechanikę.

Attributes:
    WIDTH (int): Szerokość okna gry.
    HEIGHT (int): Wysokość okna gry.
    FPS (int): Ilość renderowanych klatek na sekundę.
    BG_COLOR (touple[int, int, int]): Kolor tła w formacie RGB.
    ALPHABET (str): Polski alfabet.
    Base: Klasa będąca reprezentacją bazy deklaratywnej.
    engine (sqlalchemy.engine.Engine): Silnik bazy danych, łączący się z nią przez connection stringa.
    Session: Klasa reprezentująca sesję połączenia z bazą danych.

"""
import tkinter.messagebox as messagebox
from typing import Type

import pygame
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, declarative_base

from button import Button
from db_initialize import Category, Word, Player

WIDTH = 1600
HEIGHT = 900
FPS = 60
BG_COLOR = (9, 161, 139)
ALPHABET = "AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŻŹ"

Base = declarative_base()

engine = create_engine("sqlite:///database.db", echo=True)
Session = sessionmaker(bind=engine)


def find_indexes(letter: str, text: str) -> list[int]:
    """Znajduje wszystkie indeksy, na których znajduję się konkretny znak w napisie.

    Args:
        letter: Litera, kórej występowania szukamy.
        text: Napisa, w którym występowań litery szukamy.

    Returns:
        Lista indeksów, na których znajduję się dany znak w napisie.

    """
    indexes = []
    for i, char in enumerate(text):
        if char == letter:
            indexes.append(i)
    return indexes


class Game:
    """Klasa reprezentuje grę i zawiera jej całą mechanikę.

    Args:
        player1: Pierwszy gracz biorący udział w rozgrywce.
        player2: Drugi gracz biorący udział w rozgrywce.

    Attributes:
        clock (pygame.time.Clock): Zegar pomagający taktować odświerzanie klatek.
        player_font (tkinter.font.Font): Czcionka użwywana przy przy renderowaniu napisu, kogo jest tura.
        word_font (tkinter.font.Font): Czcionka użwywana przy przy renderowaniu kategorii i słowa.
        is_running (bool): Prawda, jeżeli rogrywka ma trwać nadal.
        images (list[pygame.Surface]): Lista zawierająca obrazki ze stanem wisielca.
        screen (pygame.Surface): Powierzchnia będąca głównym ekranem gry.
        difficulty (int): Poziom trudności: 0 - klasyczny, 1 - hradcore.
        current_step (int): Obecny stan wisielca 0 - 10.
        players (list[Player]): Lista zawierająca graczy biorących udział w rozgrywce.
        current_player (int): Indeks obecnego gracza (z listy players).
        session (sqlalchemy.orm.Session): Sesja połączenia do bazy danych.
        category (Category): Kategoria zgadywanego słowa.
        word (Word): Zgadywane sowo.
        category_string (str): Kategoria zgadywanego słowa w postaci napisu.
        word_string (str): Zgadywane sowo w postaci napisu.
        letters_remaining (int): Liczba liter, kórych brakuje do zgadnięcia słowa.
        guessed_word_list (list[str]: Reprezentacja zgadniętych liter, w przypadku niezgadniętych jest "_".
        guessed_word (str): Reprezentacja guessed_word_list w postaci napisu.
        winner (Player): Zwycięzca.
        hangman_surface (pygame.Surface): Powierzchnia z wisielcem.
        hangman_rect (pygame.Rect): Prostokąt z powierzchnią z wisielcem.
        current_player_surface (pygame.Surface): Powierzchnia z napisem, kogo jest tura.
        current_player_rect (pygame.Rect): Prostokąt z powierzchnią z napisem, kogo jest tura.
        category_surface (pygame.Surface): Powierzchnia z napisem zawierającym kategorię.
        category_rect (pygame.Rect): Prostokąt z powierzchnią z napisem zawierającym kategorię.
        guessed_word_surface (pygame.Surface): Powierzchnia z napisem zawierającym guessed_word.
        guessed_word_rect (pygame.Rect): Prostokąt z powierzchnią z napisem zawierającym guessed_word.
        buttons (list[Button]): Lista zwierające wszystkie przyciski z literami.

    """

    def __init__(self, player1: Player, player2: Player) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()
        self.player_font = pygame.font.SysFont("Comic sans MS", 50)
        self.word_font = pygame.font.SysFont("Comic sans MS", 40)
        self.is_running = True
        self.images = [pygame.image.load(f"img/{i}.png") for i in range(11)]

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Wisielec")
        pygame.display.set_icon(pygame.image.load("img/icon.png"))

        self.difficulty = 0
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
        """Odpala grę w pętli."""
        print(f"Poziom trudności: {self.difficulty}")
        while self.is_running:
            self.check_input()
            self.draw_content()
            self.check_finish()
            self.clock.tick(FPS)

        pygame.quit()

    def check_input(self) -> None:
        """Sprawdza input gracza w event loopie"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.collidepoint(event.pos):
                        if self.difficulty == 0:
                            button.is_visible = False

                        self.check_letter(button)
                        self.change_player()

    def check_letter(self, button: Button) -> None:
        """Sprawdza, czy litera na klikniętym przycisku jest w słowie. Jeżeli nie, to rysujemy wysielca.

        Args:
            button: Przycisk, którego litera jest sprawdzana.

        """
        if button.letter in self.word_string:
            indexes = find_indexes(button.letter, self.word_string)
            for index in indexes:
                self.guessed_word_list[index] = button.letter
                self.guessed_word = self.get_guessed_word()
                self.letters_remaining -= 1
        elif self.current_step <= 11:
            self.current_step += 1

    def draw_content(self) -> None:
        """Rysuje całą zwartość gry."""
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
        """Inicjuje wszysktie przyciski z literami do atrybutu buttons."""
        horizontal_offset = 200
        vertical_offset = 100
        alphabet_letter_number = 0
        for i in range(8):
            for j in range(4):
                self.buttons.append(Button(800 + (j * horizontal_offset), 100 + (i * vertical_offset), 50, 50,
                                           ALPHABET[alphabet_letter_number], self.screen))
                alphabet_letter_number += 1

    def get_guessed_word(self) -> str:
        """Zamienia atrybut guessed_word _list na napis

        Returns:
            Zgadywane słowo z brakującymi literami w postaci "_" jako napis.
        """
        result = ""
        for letter in self.guessed_word_list:
            result += letter
            result += " "
        return result

    def check_finish(self) -> None:
        """Sprawdza czy gra się skończyła.

        Po ygranej funckaj dodaje zwycięzscy +1 do wyników.
        """
        if self.current_step == 10:
            self.is_running = False
            self.winner = self.players[self.current_player]
            self.winner.add_win()
            messagebox.showinfo("Gratulacje", f"Wygrał gracz: {self.winner.nickname}")
        elif self.letters_remaining <= 0:
            self.change_player()
            self.is_running = False
            self.winner = self.players[self.current_player]
            self.winner.add_win()
            messagebox.showinfo("Gratulacje", f"Wygrał gracz: {self.winner.nickname}")

    def change_player(self) -> None:
        """Zmienia turę gracza."""
        if self.current_player == 0:
            self.current_player = 1
        elif self.current_player == 1:
            self.current_player = 0

    def pick_category_and_word(self) -> tuple[Type[Category] | None, Type[Word] | None]:
        """Losuje z bazy danych kategorię oraz związane z nią słowo.

        Returns:
            Kategoria oraz związane z nią słowo.
        """
        category = self.session.query(Category).order_by(func.random()).first()
        word = self.session.query(Word).filter_by(category_id=category.id).order_by(func.random()).first()
        return category, word
