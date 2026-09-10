from pathlib import Path

import pygame


class MusicController:
    def __init__(
        self,
        music_path: str | Path,
        target_volume: float = 0.7,
        loop: bool = False,
    ) -> None:
        self.music_path = Path(music_path)
        self.target_volume = max(0.0, min(1.0, target_volume))
        self.loop = loop

        if not self.music_path.is_file():
            raise FileNotFoundError(
                f"Music file not found: {self.music_path}"
            )

        pygame.mixer.music.load(str(self.music_path))

        self._current_volume = 0.0
        self._fade_target = 0.0
        self._fade_speed = 0.0

        pygame.mixer.music.set_volume(0.0)

    def update(self, delta_time: float) -> None:
        if self._current_volume == self._fade_target:
            return

        change = self._fade_speed * delta_time

        if self._current_volume < self._fade_target:
            self._current_volume = min(
                self._current_volume + change,
                self._fade_target,
            )
        else:
            self._current_volume = max(
                self._current_volume - change,
                self._fade_target,
            )

        pygame.mixer.music.set_volume(self._current_volume)

        if (
            self._current_volume == 0.0
            and self._fade_target == 0.0
        ):
            pygame.mixer.music.stop()

    def fade_in(self, duration: float) -> None:
        if not pygame.mixer.music.get_busy():
            loops = -1 if self.loop else 0
            pygame.mixer.music.play(loops=loops)

        self._fade_target = self.target_volume

        if duration <= 0:
            self.set_volume_immediate(self.target_volume)
            return

        self._fade_speed = (
            abs(self.target_volume - self._current_volume)
            / duration
        )

    def fade_out(self, duration: float) -> None:
        self._fade_target = 0.0

        if duration <= 0:
            self.set_volume_immediate(0.0)
            pygame.mixer.music.stop()
            return

        self._fade_speed = self._current_volume / duration

    def set_volume_immediate(self, volume: float) -> None:
        self._current_volume = max(0.0, min(1.0, volume))
        self._fade_target = self._current_volume

        pygame.mixer.music.set_volume(self._current_volume)
