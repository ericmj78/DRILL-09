"""DRILL #9: 방향키로 소년을 움직이는 pico2d 프로그램."""

import os

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


def main():
    previous_directory = os.getcwd()
    os.chdir(os.path.dirname(__file__) or '.')
    try:
        open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
        try:
            background = load_image('TUK_GROUND.png')
            running = True
            while running:
                for event in get_events():
                    if event.type == SDL_QUIT or (
                        event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE
                    ):
                        running = False
                if not running:
                    break
                clear_canvas()
                background.draw(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)
                update_canvas()
                delay(1 / 60)
        finally:
            close_canvas()
    finally:
        os.chdir(previous_directory)

if __name__ == '__main__':
    main()
