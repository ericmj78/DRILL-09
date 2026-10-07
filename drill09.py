"""DRILL #9: 방향키로 소년을 움직이는 pico2d 프로그램."""

import os
from dataclasses import dataclass, field
from math import hypot

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
IDLE_LEFT_ROW = 2
RUN_RIGHT_ROW = 1
RUN_LEFT_ROW = 0
DRAW_SIZE = 160
MOVE_SPEED = 240.0
FRAME_COUNT = 8
FRAME_INTERVAL = 0.1
DIRECTION_KEYS = frozenset((SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN))


@dataclass
class GameState:
    x: float = CANVAS_WIDTH / 2
    y: float = CANVAS_HEIGHT / 2
    facing: str = 'right'
    animation_row: int = IDLE_RIGHT_ROW
    frame_index: int = 0
    frame_elapsed: float = 0.0
    running: bool = True
    pressed_keys: set[int] = field(default_factory=set)


def input_axes(pressed_keys):
    horizontal = int(SDLK_RIGHT in pressed_keys) - int(SDLK_LEFT in pressed_keys)
    vertical = int(SDLK_UP in pressed_keys) - int(SDLK_DOWN in pressed_keys)
    return horizontal, vertical


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
                horizontal, vertical = input_axes(state.pressed_keys)
                if horizontal > 0:
                    state.facing = 'right'
                elif horizontal < 0:
                    state.facing = 'left'
                direction_length = hypot(horizontal, vertical)
                if direction_length:
                    state.x += horizontal / direction_length * MOVE_SPEED * dt
                    state.y += vertical / direction_length * MOVE_SPEED * dt
                if direction_length:
                    next_row = RUN_RIGHT_ROW if state.facing == 'right' else RUN_LEFT_ROW
                else:
                    next_row = IDLE_RIGHT_ROW if state.facing == 'right' else IDLE_LEFT_ROW
                if next_row != state.animation_row:
                    state.animation_row = next_row
                    state.frame_index = 0
                    state.frame_elapsed = 0.0
                else:
                    state.frame_elapsed += dt
                    while state.frame_elapsed >= FRAME_INTERVAL:
                        state.frame_elapsed -= FRAME_INTERVAL
                        state.frame_index = (state.frame_index + 1) % FRAME_COUNT
                clear_canvas()
                background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
                character.clip_draw(SHEET_PADDING + state.frame_index * CELL_SIZE, SHEET_PADDING + state.animation_row * CELL_SIZE, CELL_SIZE, CELL_SIZE, state.x, state.y, DRAW_SIZE, DRAW_SIZE)
                update_canvas()
                delay(1 / 60)
        finally:
            close_canvas()
    finally:
        os.chdir(previous_directory)

if __name__ == '__main__':
    main()
