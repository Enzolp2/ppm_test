import curses
from curses import wrapper
import time
import random


def start_screen(stdscr):
    stdscr.clear()
    stdscr.addstr("Bem Vindo ao teste de PPM! -> Palavras Por Minuto")
    stdscr.addstr("\nPressione qualquer tecla para iniciar o jogo.")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, ppm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0, f'PPM: {ppm}')
    for i, char in enumerate(current):
        correct_char = target[i]
        if correct_char == char:
            stdscr.addstr(0, i, char, curses.color_pair(1))
        else:
            stdscr.addstr(0, i, char, curses.color_pair(2))

def load_text():
    with open("text.txt", "r") as arquivo:
        linhas = arquivo.readlines()
        return random.choice(linhas).strip()

def ppm_test(stdscr):
    target_text = load_text()
    current_text = []
    ppm = 0
    start_time = time.time()
    stdscr.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        ppm = round(len(current_text)/(time_elapsed/60) / 5)

        stdscr.clear()
        display_text(stdscr, target_text, current_text, ppm)
        stdscr.refresh()

        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        try:
            key = stdscr.getkey()
        except:
            continue

        if ord(key) == 27:
            break
        elif key in ("KEY_BACKSPACE", '\b', "\x7f"):
            if len(current_text) > 0:
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdscr)

    while True:
        ppm_test(stdscr)
        stdscr.addstr(2, 0, "Press any button to try again...")
        key = stdscr.getkey()
        if ord(key) == 27:
            break

wrapper(main)
