import pygame
from pathlib import Path


from text_controller import (
    DemoController,
    StarfieldController,
    TextController,
    MusicController,
)


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
TARGET_FPS = 60


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode(
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Python TextController")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 72)

    starfield_controller = StarfieldController(
        viewport_size=(SCREEN_WIDTH, SCREEN_HEIGHT),
    )

    text_controller = TextController(
        text="",
        font=font,
        position=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2),
        viewport_size=(SCREEN_WIDTH, SCREEN_HEIGHT),
        color=pygame.Color("white"),
        character_spacing=4,
    )

    music_path = (
        Path(__file__).resolve().parent
        / "text_controller"
        / "Music"
        / "SidewinderRainbow.mp3"
    )

    music_controller = MusicController(
        music_path=music_path,
        target_volume=0.7,
        loop=False,
    )

    demo_controller = DemoController(
        text_controller=text_controller,
        starfield_controller=starfield_controller,
        music_controller=music_controller,
    )

    running = True

    while running:
        delta_time = clock.tick(TARGET_FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        demo_controller.update(delta_time)
        music_controller.update(delta_time)
        starfield_controller.update(delta_time)
        text_controller.update(delta_time)

        screen.fill(pygame.Color("black"))
        starfield_controller.draw(screen)
        text_controller.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()

