import tkinter.font

import pygame


class Button(pygame.Rect):
    """Klasa reprezentuje przycisk z literą.

    Args:
        left (int): Współrzędna x lewego górnego rogu przycisku.
        top (int): Współrzędna y lewego górnego rogu przycisku.
        width (int): Szerokość przycisku.
        height (int): Wysokość przycisku.
        letter (str): Litera znajdująca się na przycisku.
        surface (pygame.Surface): Powierzchnia, na której przycisk ma być rysowany.

    Attributes:
        letter (str): Litera znajdująca się na przycisku.
        surface (pygame.Surface): Powierzchnia, na której przycisk ma być rysowany.
        is_visible (bool): Prawda, jeżeli przycisk ma być widoczny i ma działać w aplikacji.
        color_rgb (tuple[int, int, int]): Kolor w formacie RGB.
        font (tkinter.font.Font): Czcionka użyta przy renderowaniu litery.
        letter_surface (pygame.Surface): Powierzchnia, na której renderowana jest litera.
    """

    def __init__(self, left: int, top: int, width: int, height: int, letter: str, surface: pygame.Surface) -> None:
        super().__init__(left, top, width, height)

        self.letter = letter
        self.surface = surface
        self.is_visible = True
        self.color_rgb = (100, 161, 139)
        self.font = pygame.font.SysFont("Comic sans MS", 35)
        self.letter_surface = self.font.render(letter, True, "black")
        self.letter_rect = self.letter_surface.get_rect(center=self.center)

    def draw(self) -> None:
        if self.is_visible:
            pygame.draw.rect(self.surface, self.color_rgb, self)
            self.surface.blit(self.letter_surface, self.letter_rect)
