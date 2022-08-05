from graphics import Window
from game import Game
# from player import Player


def run():
    # player_1 = Player('X', 'human')
    # player_2 = Player('O', 'human')
    # game = Game(player_1, player_2)
    game = Game('X', 'O')
    window = Window(game)

    window.end()


if __name__ == '__main__':
    run()
