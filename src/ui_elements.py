from typing import Callable, List, Optional, Tuple
import pygame


class Button:
    def __init__(
        self,
        position: Tuple[int, int],
        size: Tuple[int, int],
        on_click: Optional[Callable[[], None]] = None,
        color: pygame.Color = pygame.Color("#f0f0f0"),
        hover_color: pygame.Color = pygame.Color("#f0f0f0"),
        text: str = "",
        font: str = "Segoe UI",
        font_size: int = 16,
        font_color: pygame.Color = pygame.Color("black"),
    ):
        self.color = color
        self.size = size
        self.on_click = on_click
        self.surface = pygame.Surface(size)
        self.rect = self.surface.get_rect(topleft=position)
        self.hover_color = hover_color

        if len(color) == 4:
            self.surface.set_alpha(color[3])

        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.font_color = font_color
        self.text_surface = self.font.render(self.text, 1, self.font_color)
        self.text_rect = self.text_surface.get_rect(
            center=[wh // 2 for wh in self.size]
        )

    def set_text(self, text: str):
        self.text = text
        self.text_surface = self.font.render(self.text, 1, self.font_color)
        self.text_rect = self.text_surface.get_rect(
            center=[wh // 2 for wh in self.size]
        )

    def draw(self, screen: pygame.Surface):
        self.mouseover()

        self.surface.fill(self.cur_color)
        self.surface.blit(self.text_surface, self.text_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.cur_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.cur_color = self.hover_color

    def handle_click(self, mouse_pos: Tuple[int, int]):
        if self.rect.collidepoint(mouse_pos) and self.on_click:
            self.on_click()


class Text:
    def __init__(
        self,
        text: str,
        position: Tuple[int, int],
        color: pygame.Color = pygame.Color("black"),
        font: str = "Segoe UI",
        font_size: int = 15,
        middle: bool = False,
    ):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(text, 1, color)

        if len(color) == 4:
            self.text_surface.set_alpha(color[3])

        if middle:
            self.position = self.text_surface.get_rect(center=position)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.text_surface, self.position)
