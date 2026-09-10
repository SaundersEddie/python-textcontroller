import math
from enum import Enum, auto
import colorsys

import pygame


class MovementMode(Enum):
    NONE = auto()
    SCROLL_LEFT = auto()
    SCROLL_RIGHT = auto()
    SCROLL_UP = auto()
    SCROLL_DOWN = auto()
    BOUNCE_HORIZONTAL = auto()
    BOUNCE_VERTICAL = auto()


class TextEffect(Enum):
    NONE = auto()
    SINE_WAVE = auto()

class ColorEffect(Enum):
    STATIC = auto()
    FADE = auto()
    CYCLE = auto()

class TextController:
    def __init__(
        self,
        text: str,
        font: pygame.font.Font,
        position: tuple[float, float],
        viewport_size: tuple[int, int],
        color: pygame.Color | tuple[int, int, int] = pygame.Color("white"),
        character_spacing: float = 0.0,
    ) -> None:
        self.text = text
        self.font = font
        self.position = pygame.Vector2(position)
        self.viewport_size = viewport_size
        self.color = pygame.Color(color)
        self.secondary_color = pygame.Color("red")
        self.color_effect = ColorEffect.STATIC
        self.color_speed = 2.0
        self.character_spacing = character_spacing

        self.movement_mode = MovementMode.NONE
        self.movement_speed = 100.0
        self.bounce_distance = 30.0
        self.bounce_speed = 3.0

        self._offset = pygame.Vector2()
        self._bounce_origin = pygame.Vector2()
        self.text_effect = TextEffect.NONE
        self.sine_amplitude = 20.0
        self.sine_frequency = 0.6
        self.sine_speed = 4.0
        self._movement_elapsed = 0.0
        self._effect_time = 0.0

        self._character_surfaces: list[pygame.Surface] = []
        self._text_width = 0.0
        self._text_height = 0.0

        self._current_opacity = 1.0
        self._target_opacity = 1.0
        self._opacity_fade_speed = 0.0

        self._build_text()

    def _build_text(self) -> None:
        self._render_characters([self.color] * len(self.text))

    def _render_characters(
        self,
        colors: list[pygame.Color],
    ) -> None:
        self._character_surfaces = [
            self.font.render(character, True, character_color)
            for character, character_color in zip(self.text, colors)
        ]

        widths = [
            surface.get_width() for surface in self._character_surfaces
        ]

        spacing_width = max(0, len(widths) - 1) * self.character_spacing

        self._text_width = sum(widths) + spacing_width
        self._text_height = max(
            (surface.get_height() for surface in self._character_surfaces),
            default=0,
        )

    def update(self, delta_time: float) -> None:
        self._movement_elapsed += delta_time
        self._effect_time += delta_time
        self._update_color_effect()
        self._update_opacity(delta_time)

        match self.movement_mode:
            case MovementMode.NONE:
                pass

            case MovementMode.SCROLL_LEFT:
                self._offset.x -= self.movement_speed * delta_time
                self._wrap_scroll_left()

            case MovementMode.SCROLL_RIGHT:
                self._offset.x += self.movement_speed * delta_time
                self._wrap_scroll_right()

            case MovementMode.SCROLL_UP:
                self._offset.y -= self.movement_speed * delta_time
                self._wrap_scroll_up()

            case MovementMode.SCROLL_DOWN:
                self._offset.y += self.movement_speed * delta_time
                self._wrap_scroll_down()

            case MovementMode.BOUNCE_HORIZONTAL:
                self._offset.x = (
                    self._bounce_origin.x
                    + math.sin(self._movement_elapsed * self.bounce_speed)
                    * self.bounce_distance
                )

            case MovementMode.BOUNCE_VERTICAL:
                self._offset.y = (
                    self._bounce_origin.y
                    + math.sin(self._movement_elapsed * self.bounce_speed)
                    * self.bounce_distance
                )

    def draw(self, target_surface: pygame.Surface) -> None:
        center = self.position + self._offset

        draw_x = center.x - self._text_width / 2
        base_y = center.y - self._text_height / 2

        alpha = round(self._current_opacity * 255)

        for index, character_surface in enumerate(
            self._character_surfaces
        ):
            draw_y = base_y

            if self.text_effect == TextEffect.SINE_WAVE:
                draw_y += (
                    math.sin(
                        self._effect_time * self.sine_speed
                        + index * self.sine_frequency
                    )
                    * self.sine_amplitude
                )

            character_surface.set_alpha(alpha)
            target_surface.blit(character_surface, (draw_x, draw_y))

            draw_x += (
                character_surface.get_width()
                + self.character_spacing
            )

    def _wrap_scroll_left(self) -> None:
        center_x = self.position.x + self._offset.x

        if center_x + self._text_width / 2 < 0:
            self._offset.x = (
                self.viewport_size[0]
                + self._text_width / 2
                - self.position.x
            )

    def _wrap_scroll_right(self) -> None:
        center_x = self.position.x + self._offset.x

        if center_x - self._text_width / 2 > self.viewport_size[0]:
            self._offset.x = -self._text_width / 2 - self.position.x

    def _wrap_scroll_up(self) -> None:
        center_y = self.position.y + self._offset.y

        if center_y + self._text_height / 2 < 0:
            self._offset.y = (
                self.viewport_size[1]
                + self._text_height / 2
                - self.position.y
            )

    def _wrap_scroll_down(self) -> None:
        center_y = self.position.y + self._offset.y

        if center_y - self._text_height / 2 > self.viewport_size[1]:
            self._offset.y = -self._text_height / 2 - self.position.y

    def set_text(self, text: str) -> None:
        self.text = text
        self._build_text()

    def set_color(
        self,
        color: pygame.Color | tuple[int, int, int],
    ) -> None:
        self.color = pygame.Color(color)
        self._build_text()

    def set_position(self, position: tuple[float, float]) -> None:
        self.position.update(position)

    def set_movement(self, mode: MovementMode) -> None:
        if mode == self.movement_mode:
            return

        self.movement_mode = mode
        self._bounce_origin.update(self._offset)
        self._movement_elapsed = 0.0

    def set_movement_speed(self, speed: float) -> None:
        self.movement_speed = max(0.0, speed)

    def set_bounce_distance(self, distance: float) -> None:
        self.bounce_distance = max(0.0, distance)

    def set_bounce_speed(self, speed: float) -> None:
        self.bounce_speed = max(0.0, speed)

    def center_text(self) -> None:
        self._offset.update(0.0, 0.0)
        self._bounce_origin.update(0.0, 0.0)
        self._movement_elapsed = 0.0

    def position_at_scroll_start(self) -> None:
        match self.movement_mode:
            case MovementMode.SCROLL_LEFT:
                center_x = self.viewport_size[0] + self._text_width / 2
                self._offset.x = center_x - self.position.x

            case MovementMode.SCROLL_RIGHT:
                center_x = -self._text_width / 2
                self._offset.x = center_x - self.position.x

            case MovementMode.SCROLL_UP:
                center_y = self.viewport_size[1] + self._text_height / 2
                self._offset.y = center_y - self.position.y

            case MovementMode.SCROLL_DOWN:
                center_y = -self._text_height / 2
                self._offset.y = center_y - self.position.y


    def _update_color_effect(self) -> None:
        if self.color_effect == ColorEffect.STATIC:
            return

        if self.color_effect == ColorEffect.FADE:
            amount = (
                math.sin(self._effect_time * self.color_speed) + 1.0
            ) * 0.5

            current_color = self.color.lerp(
                self.secondary_color,
                amount,
            )

            self._render_characters(
                [current_color] * len(self.text)
            )
            return

        colors = []

        for index in range(len(self.text)):
            hue = (
                self._effect_time * self.color_speed * 0.1
                + index / max(len(self.text), 1)
            ) % 1.0

            red, green, blue = colorsys.hsv_to_rgb(hue, 1.0, 1.0)

            colors.append(
                pygame.Color(
                    round(red * 255),
                    round(green * 255),
                    round(blue * 255),
                )
            )

        self._render_characters(colors)

    def _update_opacity(self, delta_time: float) -> None:
        if math.isclose(
                self._current_opacity,
                self._target_opacity,
                abs_tol=0.001,
        ):
            self._current_opacity = self._target_opacity
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

    def set_text_effect(self, effect: TextEffect) -> None:
        self.text_effect = effect

    def set_color_effect(self, effect: ColorEffect) -> None:
        self.color_effect = effect

        if effect == ColorEffect.STATIC:
            self._build_text()

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

