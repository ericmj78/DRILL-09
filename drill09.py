"""DRILL #9: 방향키로 소년을 움직이는 pico2d 프로그램."""

import os
from dataclasses import dataclass

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    clear_canvas,
    close_canvas,
    delay,
    get_events,
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


@dataclass
class GameState:
    x: float = CANVAS_WIDTH / 2
    y: float = CANVAS_HEIGHT / 2
    facing: str = 'right'
    running: bool = True


def main():
    previous_directory = os.getcwd()
    os.chdir(os.path.dirname(__file__) or '.')
    try:
        open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        try:
            background = load_image('TUK_GROUND.png')
            character = load_image('animation_sheet.png')
            state = GameState()
            while state.running:
                for event in get_events():
                    if event.type == SDL_QUIT or (
                        event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                    ):
                        state.running = False
                if not state.running:
                    break
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
