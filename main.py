from graphics import Window
from game import Game
from player import Player


def run():
    window = Window()
    player_1 = Player('X')
    player_2 = Player('O')
    game = Game(player_1, player_2)
    for i in range(42):
        game.play_one_turn()
    window.render_grid(game.grid)
    window.end()


if __name__ == '__main__':
    run()
