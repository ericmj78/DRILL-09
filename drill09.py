"""DRILL #9: 방향키로 소년을 움직이는 pico2d 프로그램."""

import os
from dataclasses import dataclass, field

from pico2d import (
    SDL_KEYDOWN,
    SDL_KEYUP,
    SDL_QUIT,
    SDLK_ESCAPE,
    SDLK_LEFT,
    SDLK_RIGHT,
    SDLK_UP,
    SDLK_DOWN,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
    get_time,
    load_image,
    open_canvas,
    update_canvas,
)

CANVAS_WIDTH = 1280
CANVAS_HEIGHT = 1024
CELL_SIZE = 100
SHEET_PADDING = 1
IDLE_RIGHT_ROW = 3
DRAW_SIZE = 160
MOVE_SPEED = 240.0
DIRECTION_KEYS = frozenset((SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN))


@dataclass
class GameState:
    x: float = CANVAS_WIDTH / 2
    y: float = CANVAS_HEIGHT / 2
    facing: str = 'right'
    running: bool = True
    pressed_keys: set[int] = field(default_factory=set)


def main():
    previous_directory = os.getcwd()
    os.chdir(os.path.dirname(__file__) or '.')
    try:
        open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        try:
            background = load_image('TUK_GROUND.png')
            character = load_image('animation_sheet.png')
            state = GameState()
            last_time = get_time()
            while state.running:
                for event in get_events():
                    if event.type == SDL_QUIT:
                        state.running = False
                    elif event.type == SDL_KEYDOWN:
                        if event.key == SDLK_ESCAPE:
                            state.running = False
                        elif event.key in DIRECTION_KEYS:
                            state.pressed_keys.add(event.key)
                    elif event.type == SDL_KEYUP:
                        state.pressed_keys.discard(event.key)
                if not state.running:
                    break
                now = get_time()
                dt = max(0.0, now - last_time)
                last_time = now
                if SDLK_RIGHT in state.pressed_keys:
                    state.x += MOVE_SPEED * dt
                if SDLK_LEFT in state.pressed_keys:
                    state.x -= MOVE_SPEED * dt
                if SDLK_UP in state.pressed_keys:
                    state.y += MOVE_SPEED * dt
                if SDLK_DOWN in state.pressed_keys:
                    state.y -= MOVE_SPEED * dt
                clear_canvas()
                background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
                character.clip_draw(SHEET_PADDING, SHEET_PADDING + IDLE_RIGHT_ROW * CELL_SIZE, CELL_SIZE, CELL_SIZE, state.x, state.y, DRAW_SIZE, DRAW_SIZE)
                update_canvas()
                delay(1 / 60)
        finally:
            close_canvas()
    finally:
        os.chdir(previous_directory)

if __name__ == '__main__':
    main()
