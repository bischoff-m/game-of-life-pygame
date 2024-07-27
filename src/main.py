from typing import List
import pygame
import sys
import numpy as np
from ui_elements import Button

# Constants
BLACK = pygame.Color("#2f3061")
WHITE = pygame.Color("#dfdfdf")
GRID_HEIGHT = 750
GRID_WIDTH = 800
FOOTER_HEIGHT = 36
BLOCK_SIZE = 10
state = np.zeros((GRID_WIDTH // BLOCK_SIZE, GRID_HEIGHT // BLOCK_SIZE))
prev_states = np.zeros((3, state.shape[0], state.shape[1]))
ui_elements: List[Button] = []
is_paused = True


def main():
    global SCREEN, CLOCK, state, is_paused
    pygame.init()
    SCREEN = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT + FOOTER_HEIGHT))
    CLOCK = pygame.time.Clock()
    SCREEN.fill(BLACK)

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

    # Update state
    prev_states[2] = prev_states[1]
    prev_states[1] = prev_states[0]
    prev_states[0] = state.copy()
    state[:] = new_state


def draw_grid():
    for x, y in np.ndindex(state.shape):
        # Brightness ranges from 0 to 1
        brightness = state[x][y]
        brightness += 0.5 * prev_states[0][x][y]
        brightness += 0.25 * prev_states[1][x][y]
        brightness += 0.125 * prev_states[2][x][y]
        brightness = min(1, brightness)
        # Use darkness to scale color
        color = pygame.Color(
            int(WHITE.r * brightness),
            int(WHITE.g * brightness),
            int(WHITE.b * brightness),
        )
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
