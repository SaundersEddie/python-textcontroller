# Python TextController

A reusable Pygame text-effects controller inspired by old-school arcade games, C64 demo-scene effects, scrolling messages, title screens, and attract modes.

This is the Python/Pygame counterpart to:

* [Unity TextController](https://github.com/SaundersEddie/Unity-TextController)
* [Godot TextController](https://github.com/SaundersEddie/Godot-TextController)
* [C64 TextController](https://github.com/SaundersEddie/C64-TextController)

The controller renders each character separately, allowing movement, character animation, color effects, and opacity fades to operate independently and be freely combined.

## Current Features

### Movement

* None
* Scroll left
* Scroll right
* Scroll up
* Scroll down
* Horizontal bounce
* Vertical bounce
* Full off-screen wrapping

### Text Effects

* None
* Per-character sine wave

### Color Effects

* Static color
* Fade between two colors
* Per-character HSV color cycling

### Additional Controllers

* Whole-text fade in and fade out
* Runtime-generated parallax starfield
* Music playback with volume fades
* Automatic demo sequencing

Movement, text effects, and color effects are separate systems.

For example, text can scroll horizontally while each character follows a sine wave and cycles through rainbow colors.

## Requirements

* Python 3.13 or newer
* Pygame 2.6.1

The project was initially developed using:

```text
Python 3.13.15
Pygame 2.6.1
SDL 2.28.4
```

## Installation

Clone the repository:

```bash
git clone https://github.com/SaundersEddie/python-textcontroller.git
cd python-textcontroller
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Install the requirements:

```bash
python -m pip install -r requirements.txt
```

## Running the Demo

Run:

```bash
python main.py
```

The demo runs at:

```text
1920 × 1080
60 FPS
```

Press `Escape` or close the window to exit.

The sequence runs automatically and demonstrates scrolling, bouncing, sine-wave movement, color cycling, opacity fades, music, and the parallax starfield.

## Project Structure

```text
python-textcontroller/
├── main.py
├── requirements.txt
├── README.md
└── text_controller/
    ├── __init__.py
    ├── demo_controller.py
    ├── music_controller.py
    ├── starfield_controller.py
    ├── text_controller.py
    └── Music/
        └── SidewinderRainbow.mp3
```

## TextController

`TextController` manages:

* Text content
* Per-character rendering
* Whole-text movement
* Sine-wave character offsets
* Static and animated colors
* Whole-text opacity

Basic construction:

```python
text_controller = TextController(
    text="HELLO WORLD",
    font=font,
    position=(960, 540),
    viewport_size=(1920, 1080),
    color=pygame.Color("white"),
    character_spacing=4,
)
```

The controller is updated and drawn from the main Pygame loop:

```python
text_controller.update(delta_time)
text_controller.draw(screen)
```

### Movement Example

```python
text_controller.set_movement_speed(250)
text_controller.set_movement(MovementMode.SCROLL_LEFT)
text_controller.position_at_scroll_start()
```

### Sine-Wave Example

```python
text_controller.set_text_effect(TextEffect.SINE_WAVE)

text_controller.sine_amplitude = 20
text_controller.sine_frequency = 0.6
text_controller.sine_speed = 4
```

### Color-Cycle Example

```python
text_controller.set_color_effect(ColorEffect.CYCLE)
text_controller.color_speed = 2
```

### Combined Example

```python
text_controller.set_movement(MovementMode.SCROLL_LEFT)
text_controller.set_text_effect(TextEffect.SINE_WAVE)
text_controller.set_color_effect(ColorEffect.CYCLE)
```

This produces a traditional horizontally scrolling, rainbow-colored sine wave.

Use responsibly.

Or don’t.

## Public Controls

The current public methods include:

```python
set_text(text)
set_color(color)
set_position(position)

set_movement(mode)
set_movement_speed(speed)

set_bounce_distance(distance)
set_bounce_speed(speed)

set_text_effect(effect)
set_color_effect(effect)

position_at_scroll_start()
center_text()

fade_in(duration)
fade_out(duration)
set_opacity_immediate(opacity)
```

## Internal Architecture

Each character is rendered as an individual Pygame surface.

Whole-text movement is applied to the combined text position, while character effects apply an additional offset to each character during drawing.

Conceptually:

```text
TextController
└── Character surfaces
    ├── Character 1
    ├── Character 2
    ├── Character 3
    └── ...
```

Responsibilities remain separated:

```text
TextController      -> text, movement, text effects, color, opacity
StarfieldController -> star generation, movement, wrapping, opacity
MusicController     -> music playback, looping, volume fades
DemoController      -> automatic sequence and timing
main.py              -> Pygame setup, event loop, updating and drawing
```

## Coordinate Handling

Scrolling checks the complete rendered width or height of the text.

The controller waits until the entire string has left the visible area before repositioning it beyond the opposite edge.

This prevents text from:

* Disappearing before the final character leaves the screen
* Respawning while part of the string is still visible
* Wrapping relative to the wrong coordinate system

## Fonts

The current demo uses Pygame’s default font.

A custom `.ttf` or `.otf` font can be loaded with:

```python
font = pygame.font.Font("path/to/font.ttf", 72)
```

A retro font may be added later, but no custom font is required to use the controller.

## Music

The demo currently expects:

```text
text_controller/Music/SidewinderRainbow.mp3
```

The music controller supports:

* Target playback volume
* Optional looping
* Fade in
* Fade out
* Immediate volume changes
* Automatic stopping after fading to silence

The included music remains separate from the source-code license and may not be reused or redistributed independently without permission.

## Design Goals

The project is intended to remain:

* Self-contained
* Reusable
* Easy to configure
* Independent of a specific game
* Free from hand-built character objects
* Suitable for retro games, title screens, messages, and demo sequences

The primary component remains `TextController`. The starfield, music, and demo controllers are optional supporting components.

## Future Possibilities

Possible later additions include:

* Custom font bundled with the demo
* Palette-based color cycling
* Typewriter effects
* Character rotation
* Character scaling and pulsing
* Additional wave effects
* Start and restart delays
* Loop counters and completion events
* Automated tests
* Formal Python package distribution

## License

Python TextController is released as freeware source.

You may read, study, modify, and use the source for personal projects, learning, experimentation, content creation, and internal tooling.

Third-party assets and audio assets remain under their own licenses. Check the relevant asset license before reusing or redistributing them.

This project is provided as-is, without warranty or a support guarantee.

## Author

Created by Eddie Saunders.

* Website: [eddiesaunders.com](https://eddiesaunders.com/)
* Code and tools: [eddiesaunders.com/code](https://eddiesaunders.com/code)
* Games: [eddiesgames.xyz](https://eddiesgames.xyz/)
* YouTube: [One Grid at a Time](https://www.youtube.com/@onegridatatime)

## Optional Support

Python TextController remains free to use.

If you find it useful and want to support more small utilities, OGaaT content, and Eddie Saunders projects, you can optionally buy me a coffee:

[paypal.me/edwynsaunders1](https://paypal.me/edwynsaunders1)
