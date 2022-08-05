from random import randrange
from player import Player


class Game:
    def __init__(self, player_1: Player, player_2: Player, starting_player: Player | None = None):
        self.players = [player_1, player_2]
        self.grid = [['-' for _ in range(7)] for _ in range(6)]
        if starting_player is None:
            self.current_player = [player_1, player_2][randrange(2)]
        else:
            self.current_player = starting_player

    def play_one_turn(self):
        move = self.current_player.get_next_move(self.grid)
        self.make_move(move, self.current_player.tag)
        winner = self.get_winner()
        if winner:
            self.winner_end(winner)
            return
        elif self.no_more_possible_moves():
            self.tie_end()
            return
        self.change_player()

    def change_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def no_more_possible_moves(self):
        return all([self.grid[0][i] != '-' for i in range(7)])

    @staticmethod
    def winner_end(winner):
        print('Game is over!', winner, 'wins!')

    @staticmethod
    def tie_end():
        print('Game is over! There are no more possible moves!')

    def make_move(self, move, tag):
        for i in range(5, -1, -1):
            if self.grid[i][move] == '-':
                self.grid[i][move] = tag
                return


    @staticmethod
    def get_winner():
        if Game.connect_4('X'):
            return 'X'
        if Game.connect_4('O'):
            return 'O'
        return None

    @staticmethod
    def connect_4(tag):
        return False  # TODO
