from dataclasses import dataclass

import pygame

from .starfield_controller import StarfieldController
from .text_controller import (
    ColorEffect,
    MovementMode,
    TextController,
    TextEffect,
)

from .music_controller import MusicController

@dataclass(frozen=True)
class DemoStep:
    text: str
    duration: float
    movement: MovementMode = MovementMode.NONE
    text_effect: TextEffect = TextEffect.NONE
    color_effect: ColorEffect = ColorEffect.STATIC
    movement_speed: float = 200.0
    bounce_distance: float = 30.0
    bounce_speed: float = 3.0
    fade_duration: float = 1.0


class DemoController:
    def __init__(
        self,
        text_controller: TextController,
        starfield_controller: StarfieldController,
        music_controller: MusicController,
    ) -> None:
        self.text_controller = text_controller
        self.starfield_controller = starfield_controller
        self.music_controller = music_controller

        self._steps = [
            DemoStep(
                text="PYTHON TEXT CONTROLLER",
                duration=7.0,
            ),
            DemoStep(
                text="CODER: SOME HIPPY FROM ENGLAND",
                duration=7.0,
            ),
            DemoStep(
                text="SCROLL LEFT",
                duration=7.5,
                movement=MovementMode.SCROLL_LEFT,
                movement_speed=320.0,
            ),
            DemoStep(
                text="SCROLL RIGHT",
                duration=7.75,
                movement=MovementMode.SCROLL_RIGHT,
                movement_speed=320.0,
            ),
            DemoStep(
                text="SINE WAVE",
                duration=7.5,
                text_effect=TextEffect.SINE_WAVE,
            ),
            DemoStep(
                text="SINE WAVE + COLOR CYCLE",
                duration=8.0,
                text_effect=TextEffect.SINE_WAVE,
                color_effect=ColorEffect.CYCLE,
            ),
            DemoStep(
                text="BOUNCE HORIZONTAL",
                duration=7.5,
                movement=MovementMode.BOUNCE_HORIZONTAL,
                bounce_distance=300.0,
                bounce_speed=4.0,
            ),
            DemoStep(
                text="BOUNCE VERTICAL",
                duration=7.75,
                movement=MovementMode.BOUNCE_VERTICAL,
                color_effect=ColorEffect.CYCLE,
                bounce_distance=250.0,
                bounce_speed=2.0,
            ),
            DemoStep(
                text="SCROLL UP",
                duration=7.75,
                movement=MovementMode.SCROLL_UP,
                color_effect=ColorEffect.CYCLE,
                movement_speed=200.0,
            ),
            DemoStep(
                text="SCROLL DOWN",
                duration=8.0,
                movement=MovementMode.SCROLL_DOWN,
                text_effect=TextEffect.SINE_WAVE,
                color_effect=ColorEffect.CYCLE,
                movement_speed=200.0,
            ),
            DemoStep(
                text="WELCOME TO THE LATE 1900S",
                duration=5.0,
                text_effect=TextEffect.SINE_WAVE,
                color_effect=ColorEffect.CYCLE,
            ),
        ]

        self._state = "opening"
        self._elapsed = 0.0
        self._step_index = -1
        self._fade_out_started = False

        self.text_controller.set_opacity_immediate(0)
        self.starfield_controller.set_opacity_immediate(0)
        self.starfield_controller.fade_in(2.0)
        self.music_controller.set_volume_immediate(0)
        self.music_controller.fade_in(2.0)

    def update(self, delta_time: float) -> None:
        self._elapsed += delta_time

        if self._state == "opening":
            if self._elapsed >= 2.0:
                self._start_step(0)
            return

        if self._state == "running":
            step = self._steps[self._step_index]

            fade_out_time = step.duration - step.fade_duration

            if (
                not self._fade_out_started
                and self._elapsed >= fade_out_time
            ):
                self.text_controller.fade_out(step.fade_duration)
                self._fade_out_started = True

            if self._elapsed >= step.duration:
                next_index = self._step_index + 1

                if next_index < len(self._steps):
                    self._start_step(next_index)
                else:
                    self._start_closing()

    def _start_step(self, index: int) -> None:
        step = self._steps[index]

        self._state = "running"
        self._step_index = index
        self._elapsed = 0.0
        self._fade_out_started = False

        self.text_controller.set_movement(MovementMode.NONE)
        self.text_controller.center_text()

        self.text_controller.set_text(step.text)
        self.text_controller.set_text_effect(step.text_effect)
        self.text_controller.set_color(pygame.Color("white"))
        self.text_controller.set_color_effect(step.color_effect)

        self.text_controller.set_movement_speed(
            step.movement_speed
        )
        self.text_controller.set_bounce_distance(
            step.bounce_distance
        )
        self.text_controller.set_bounce_speed(
            step.bounce_speed
        )

        self.text_controller.set_opacity_immediate(0)
        self.text_controller.fade_in(step.fade_duration)
        self.text_controller.set_movement(step.movement)

    def _start_closing(self) -> None:
        self._state = "closing"
        self._elapsed = 0.0

        self.text_controller.set_opacity_immediate(0)
        self.starfield_controller.fade_out(4.0)
        self.music_controller.fade_out(4.0)
