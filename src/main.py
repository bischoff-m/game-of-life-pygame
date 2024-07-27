from typing import Callable, List, Optional
import pygame
import sys
import numpy as np
from ui_elements import Button


class Gradient:
    def __init__(
        self,
        primary: pygame.Color,
        secondary: pygame.Color,
        steps: int,
        ease_func: Optional[Callable[[float], float]] = None,
    ):
        self.steps = steps
        # Calculate immediate color steps
        # 0 -> primary, steps -> secondary
        self.colors: List[pygame.Color] = []
        for i in range(steps):
            val = i / (steps - 1)
            if ease_func:
                val = ease_func(val)
            self.colors.append(primary.lerp(secondary, val))

    def get(self, step: int) -> pygame.Color:
        if step < 0 or step >= self.steps:
            raise ValueError("Step out of bounds")
        return self.colors[step]


# Constants
PRIMARY_COLOR = pygame.Color("#d49d6a")
SECONDAY_COLOR = pygame.Color("#2f4073")
GRID_HEIGHT = 750
GRID_WIDTH = 800
FOOTER_HEIGHT = 36
BLOCK_SIZE = 10
gradient = Gradient(PRIMARY_COLOR, SECONDAY_COLOR, 100, lambda x: x**0.5)
ui_elements: List[Button] = []
is_paused = False

# State of the grid
# 0 = currently active
# 1 = was active 1 step ago
# n = inactive
# Game of Life rules are applied for == 0 (active) and > 0 (inactive)
state = np.zeros((GRID_WIDTH // BLOCK_SIZE, GRID_HEIGHT // BLOCK_SIZE), dtype=int)


def main():
    global SCREEN, CLOCK
    pygame.init()
    SCREEN = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT + FOOTER_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(SECONDAY_COLOR)

    # Initialize state
    init_state_random()
    init_footer()

    # Initial draw
    draw_grid()
    draw_footer()

    # Main loop
    while True:
        CLOCK.tick(10)

        draw_footer()
        if not is_paused:
            update_state()
            draw_grid()

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
    # Set all inactive cells to max value
    state[state == 1] = gradient.steps - 1


def update_state():
    global state
    # For new_state == 1 <-> active, == 0 <-> inactive
    new_state = np.zeros_like(state)

    # Game of Life rules
    for x, y in np.ndindex(state.shape):
        # Count neighbors
        neighbors = 0
        for dx, dy in np.ndindex((3, 3)):
            if dx == 1 and dy == 1:
                continue
            new_x = x + dx - 1
            new_y = y + dy - 1
            if (
                0 <= new_x < state.shape[0]
                and 0 <= new_y < state.shape[1]
                and state[new_x][new_y] == 0
            ):
                neighbors += 1

        # Apply rules
        if state[x][y] == 0:
            if neighbors == 2 or neighbors == 3:
                new_state[x][y] = 1
        else:
            if neighbors == 3:
                new_state[x][y] = 1

    # Shift inactive cells
    state += 1
    # Set cells to 0 that are active now
    state[new_state == 1] = 0
    # Clip to max value
    state = np.clip(state, 0, gradient.steps - 1)


def draw_grid():
    for x, y in np.ndindex(state.shape):
        color = gradient.get(state[x][y])
        rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, color, rect)


def init_footer():
    padding = 4
    color = pygame.Color("#f0f0f0")
    hover_color = pygame.Color("#b0b0b0")

    def _randomize():
        init_state_random()
        draw_grid()

    button_random = Button(
        position=(padding, GRID_HEIGHT + padding),
        size=(90, FOOTER_HEIGHT - 2 * padding),
        on_click=_randomize,
        color=color,
        hover_color=hover_color,
        text="RANDOM",
    )
    ui_elements.append(button_random)

    def _toggle_pause():
        global is_paused
        is_paused = not is_paused
        button_pause.set_text("RESUME" if is_paused else "PAUSE")

    button_pause = Button(
        position=(100 + padding, GRID_HEIGHT + padding),
        size=(90, FOOTER_HEIGHT - 2 * padding),
        on_click=_toggle_pause,
        color=color,
        hover_color=hover_color,
        text="RESUME" if is_paused else "PAUSE",
    )
    ui_elements.append(button_pause)


def draw_footer():
    for element in ui_elements:
        element.draw(SCREEN)


if __name__ == "__main__":
    main()
