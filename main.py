from graphics import Window
from game import Game


def run():
    game = Game('O', 'X', starting_player='O')
    window = Window(game)
    window.end()


if __name__ == '__main__':
    run()
