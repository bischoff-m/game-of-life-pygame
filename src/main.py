from typing import List
import pygame
import sys
import numpy as np


class Button:
    def __init__(
        self,
        position,
        size,
        color=pygame.Color("#f0f0f0"),
        hover_color=pygame.Color("#f0f0f0"),
        on_click=None,
        text="",
        font="Segoe UI",
        font_size=16,
        font_color=pygame.Color("black"),
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

    def set_text(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, 1, self.font_color)
        self.text_rect = self.text_surface.get_rect(
            center=[wh // 2 for wh in self.size]
        )

    def draw(self, screen):
        self.mouseover()

        self.surface.fill(self.cur_color)
        self.surface.blit(self.text_surface, self.text_rect)
        screen.blit(self.surface, self.rect)

    def mouseover(self):
        self.cur_color = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.cur_color = self.hover_color

    def handle_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.on_click:
            self.on_click()


class Text:
    def __init__(
        self,
        text,
        position,
        color=pygame.Color("black"),
        font="Segoe UI",
        font_size=15,
        middle=False,
    ):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.text_surface = self.font.render(text, 1, color)

        if len(color) == 4:
            self.text_surface.set_alpha(color[3])

        if middle:
            self.position = self.text_surface.get_rect(center=position)

    def draw(self, screen):
        screen.blit(self.text_surface, self.position)


# Constants
BLACK = pygame.Color("#2f3061")
WHITE = pygame.Color("#dfdfdf")
GRID_HEIGHT = 750
GRID_WIDTH = 800
FOOTER_HEIGHT = 36
BLOCK_SIZE = 10
state = np.zeros((GRID_WIDTH // BLOCK_SIZE, GRID_HEIGHT // BLOCK_SIZE))
ui_elements: List[Button] = []
is_paused = False


def main():
    global SCREEN, CLOCK, state, is_paused
    pygame.init()
    SCREEN = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT + FOOTER_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

    init_state_random()
    init_footer()

    while True:
        CLOCK.tick(10)
        if not is_paused:
            update_state()
            draw_grid()
        draw_footer()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for element in ui_elements:
                    element.handle_click(pos)

        pygame.display.update()


def init_state_random():
    for x, y in np.ndindex(state.shape):
        state[x][y] = np.random.randint(0, 2)


def update_state():
    # Game of Life rules
    new_state = np.zeros_like(state)
    for x, y in np.ndindex(state.shape):
        neighbors = 0
        for dx, dy in np.ndindex((3, 3)):
            if dx == 1 and dy == 1:
                continue
            new_x = x + dx - 1
            new_y = y + dy - 1
            if 0 <= new_x < state.shape[0] and 0 <= new_y < state.shape[1]:
                neighbors += state[new_x][new_y]

        if state[x][y] == 1:
            if neighbors < 2 or neighbors > 3:
                new_state[x][y] = 0
            else:
                new_state[x][y] = 1
        else:
            if neighbors == 3:
                new_state[x][y] = 1

    state[:] = new_state


def draw_grid():
    for x, y in np.ndindex(state.shape):
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        if state[x][y] == 1:
            pygame.draw.rect(SCREEN, WHITE, rect)
        else:
            pygame.draw.rect(SCREEN, BLACK, rect)


def init_footer():
    padding = 4
    color = pygame.Color("#f0f0f0")
    hover_color = pygame.Color("#b0b0b0")

    button_random = Button(
        position=(padding, GRID_HEIGHT + padding),
        size=(90, FOOTER_HEIGHT - 2 * padding),
        color=color,
        hover_color=hover_color,
        on_click=init_state_random,
        text="RANDOM",
    )
    ui_elements.append(button_random)

    def toggle_pause():
        global is_paused
        is_paused = not is_paused
        button_pause.set_text("RESUME" if is_paused else "PAUSE")

    button_pause = Button(
        position=(100 + padding, GRID_HEIGHT + padding),
        size=(90, FOOTER_HEIGHT - 2 * padding),
        color=color,
        hover_color=hover_color,
        on_click=toggle_pause,
        text="RESUME" if is_paused else "PAUSE",
    )
    ui_elements.append(button_pause)


def draw_footer():
    for element in ui_elements:
        element.draw(SCREEN)


if __name__ == "__main__":
    main()
