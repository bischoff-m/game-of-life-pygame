from typing import Callable, Dict, List, Optional
import numpy as np
import pygame


class Gradient:
    def __init__(
        self,
        colors: Dict[float, pygame.Color],
        steps: int,
    ):
        self.steps = steps

        # Validate colors
        if len(colors) < 2:
            raise ValueError("At least two colors are required")
        if not colors.get(0) or not colors.get(1):
            raise ValueError("Colors must have keys 0 and 1")
        keys = np.asarray(list(colors.keys()))
        if not ((keys >= 0) & (keys <= 1)).all():
            raise ValueError("Keys must be between 0 and 1")

        # Convert to list of tuples
        grad_colors = sorted(colors.items())

        # Calculate immediate color steps
        # 0 -> primary, steps -> secondary
        self.color_steps: List[pygame.Color] = []
        cur_primary = 0
        for i in range(steps):
            val = i / (steps - 1)
            if (
                cur_primary < len(grad_colors) - 2
                and val >= grad_colors[cur_primary + 1][0]
            ):
                cur_primary += 1
            cur_val, cur_color = grad_colors[cur_primary]
            next_val, next_color = grad_colors[cur_primary + 1]
            self.color_steps.append(
                cur_color.lerp(next_color, (val - cur_val) / (next_val - cur_val))
            )

    def get(self, step: int) -> pygame.Color:
        if step < 0 or step >= self.steps:
            raise ValueError("Step out of bounds")
        return self.color_steps[step]
