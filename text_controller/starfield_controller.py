import random
from dataclasses import dataclass

import pygame


@dataclass
class Star:
    position: pygame.Vector2
    size: float
    speed: float


class StarfieldController:
    def __init__(
        self,
        viewport_size: tuple[int, int],
        star_count: int = 80,
        min_star_size: float = 1.0,
        max_star_size: float = 4.0,
        min_speed: float = 30.0,
        max_speed: float = 160.0,
        color: pygame.Color | tuple[int, int, int] = pygame.Color("white"),
    ) -> None:
        self.viewport_size = viewport_size
        self.color = pygame.Color(color)

        self._current_opacity = 1.0
        self._target_opacity = 1.0
        self._opacity_fade_speed = 0.0

        self._drawing_surface = pygame.Surface(
            viewport_size,
            pygame.SRCALPHA,
        )

        self._stars: list[Star] = []

        for _ in range(star_count):
            depth = random.random()

            self._stars.append(
                Star(
                    position=pygame.Vector2(
                        random.uniform(0, viewport_size[0]),
                        random.uniform(0, viewport_size[1]),
                    ),
                    size=min_star_size
                    + (max_star_size - min_star_size) * depth,
                    speed=min_speed
                    + (max_speed - min_speed) * depth,
                )
            )

    def update(self, delta_time: float) -> None:
        width, height = self.viewport_size

        for star in self._stars:
            star.position.x -= star.speed * delta_time

            if star.position.x + star.size < 0:
                star.position.x = width
                star.position.y = random.uniform(0, height)

        self._update_opacity(delta_time)

    def draw(self, target_surface: pygame.Surface) -> None:
        self._drawing_surface.fill((0, 0, 0, 0))

        alpha = round(self._current_opacity * 255)
        draw_color = (*self.color[:3], alpha)

        for star in self._stars:
            pygame.draw.circle(
                self._drawing_surface,
                draw_color,
                star.position,
                max(1, round(star.size)),
            )

        target_surface.blit(self._drawing_surface, (0, 0))

    def _update_opacity(self, delta_time: float) -> None:
        if self._current_opacity == self._target_opacity:
            return

        change = self._opacity_fade_speed * delta_time

        if self._current_opacity < self._target_opacity:
            self._current_opacity = min(
                self._current_opacity + change,
                self._target_opacity,
            )
        else:
            self._current_opacity = max(
                self._current_opacity - change,
                self._target_opacity,
            )

    def fade_in(self, duration: float) -> None:
        self._fade_to(1.0, duration)

    def fade_out(self, duration: float) -> None:
        self._fade_to(0.0, duration)

    def _fade_to(self, target: float, duration: float) -> None:
        if duration <= 0:
            self.set_opacity_immediate(target)
            return

        self._target_opacity = target
        self._opacity_fade_speed = (
            abs(self._target_opacity - self._current_opacity)
            / duration
        )

    def set_opacity_immediate(self, opacity: float) -> None:
        self._current_opacity = max(0.0, min(1.0, opacity))
        self._target_opacity = self._current_opacity
