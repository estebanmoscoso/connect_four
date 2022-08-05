from graphics import Window
from game import Game
from player import Player


def run():
    player_1 = Player('X')
    player_2 = Player('O')
    game = Game(player_1, player_2)
    window = Window(game)

    window.end()


if __name__ == '__main__':
    run()
