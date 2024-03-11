import pygame
import tkinter as tk
from tkinter import messagebox
from const.const import *
from const.colours import *
from data.classes.Board import Board
from data.classes.additions.Clock import Clock
from data.classes.additions.Button import Button


def main():
    try:
        pygame.init()
        screen = initialize_screen(WINDOW_SIZE)
        board = Board(BOARD_WIDTH, BOARD_HEIGHT)
        white_clock = Clock(x=CLOCK_X, y=WHITE_CLOCK_Y, width=CLOCK_WIDTH, height=CLOCK_HEIGHT, color=WHITE,
                            font_color=BLACK, initial_time=INITIAL_TIME)

        black_clock = Clock(x=CLOCK_X, y=BLACK_CLOCK_Y, width=CLOCK_WIDTH, height=CLOCK_HEIGHT, color=BLACK,
                            font_color=WHITE, initial_time=INITIAL_TIME)

        start_button = Button(x=START_BUTTON_X, y=START_BUTTON_Y, width=START_BUTTON_WIDTH, height=START_BUTTON_HEIGHT,
                              text="Start Game", color=BUTTON_NOT_PRESSED, font_color=WHITE, font_size=40)

        time_buttons = [Button(x=START_BUTTON_X + i * (TIME_BUTTON_WIDTH + TIME_BUTTON_MARGIN), y=TIME_BUTTON_Y,
                               width=TIME_BUTTON_WIDTH, height=TIME_BUTTON_HEIGHT,
                               text=f"{TIME_OPTIONS[i] // 60000}:00", color=BUTTON_NOT_PRESSED,
                               font_color=WHITE, font_size=20) for i in range(len(TIME_OPTIONS))]

        surrender_button = Button(x=SURRENDER_BUTTON_X, y=SURRENDER_BUTTON_Y, width=SURRENDER_BUTTON_WIDTH,
                                  height=SURRENDER_BUTTON_HEIGHT, text="Surrender", color=SURRENDER_BUTTON_COLOR,
                                  font_color=WHITE, font_size=40)

        run_game(screen, board, white_clock, black_clock, start_button, time_buttons, surrender_button)
    finally:
        pygame.quit()


def initialize_screen(window_size):
    screen = pygame.display.set_mode(window_size)
    return screen


def run_game(screen, board, white_clock, black_clock, start_button, time_buttons, surrender_button):
    running = True
    game_started = False
    clock = pygame.time.Clock()
    while running:
        running, game_started, continue_loop = handle_events(board, white_clock, black_clock, start_button,
                                                             time_buttons, surrender_button, running, game_started)
        if not continue_loop:
            break
        if game_started:
            running = update_game_state(board, white_clock, black_clock, running)
        draw(screen, board, white_clock, black_clock, start_button, time_buttons, surrender_button, game_started)
        pygame.display.update()
        clock.tick(30)


def handle_events(board, white_clock, black_clock, start_button, time_buttons, surrender_button, running, game_started):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False, game_started, False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not game_started:
                for i, button in enumerate(time_buttons):
                    if button.is_clicked(pygame.mouse.get_pos()):
                        for btn in time_buttons:
                            btn.color = BUTTON_NOT_PRESSED
                        white_clock.initial_time = TIME_OPTIONS[i]
                        black_clock.initial_time = TIME_OPTIONS[i]
                        button.color = BUTTON_PRESSED
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    game_started = True

            elif game_started:
                handle_mouse_click(board, white_clock, black_clock)
                if surrender_button.is_clicked(pygame.mouse.get_pos()):

                    if board.turn == 'white':
                        print_winner('Black')
                    else:
                        print_winner('White')
                    pygame.quit()
                    return False, game_started, False

    return running, game_started, True


def handle_mouse_click(board, white_clock, black_clock):
    mx, my = pygame.mouse.get_pos()
    board.handle_click(mx, my)
    if board.turn == 'white':
        black_clock.stop()
        white_clock.start()
    else:
        white_clock.stop()
        black_clock.start()


def update_game_state(board, white_clock, black_clock, running):
    if white_clock.initial_time <= 0:
        print_winner('Black')
        return False
    elif black_clock.initial_time <= 0:
        print_winner('White')
        return False
    if board.is_in_checkmate('black'):
        print_winner('White')
        return False
    elif board.is_in_checkmate('white'):
        print_winner('Black')
        return False
    white_clock.update()
    black_clock.update()
    return running


def draw(display, board, white_clock, black_clock, start_button, time_buttons, surrender_button, game_started):
    board.draw(display)
    white_clock.draw(display)
    black_clock.draw(display)
    if not game_started:
        pygame.draw.rect(display, LIGHT_GREY, (600, 75, 200, 450))
        start_button.color = BUTTON_NOT_PRESSED
        for button in time_buttons:
            button.draw(display)
    else:
        start_button.color = BUTTON_PRESSED
        surrender_button.draw(display)
    start_button.draw(display)


def print_winner(winner):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Game Over", f"{winner} wins!")


if __name__ == '__main__':
    main()
