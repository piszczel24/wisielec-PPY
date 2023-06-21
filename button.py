import pygame


class Button(pygame.Rect):

    def __init__(self, left: int, top: int, width: int, height: int, letter: str, surface: pygame.Surface) -> None:
        super().__init__(left, top, width, height)

        self.letter = letter
        self.surface = surface

        self.is_visible = True

        self.color_rgb = (100, 161, 139)
        self.font = pygame.font.SysFont("Comic sans MS", 40)
        self.letter_surface = self.font.render(letter, True, "black")
        self.letter_rect = self.letter_surface.get_rect(center=self.center)

    def draw(self):
        print(self.is_visible)
        pygame.draw.rect(self.surface, self.color_rgb, self)
        self.surface.blit(self.letter_surface, self.letter_rect)
