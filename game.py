from random import randrange
from player import Player


class Game:
    def __init__(self, player_1: Player, player_2: Player, starting_player: Player | None = None):
        self.players = [player_1, player_2]
        self.grid = [['-' for _ in range(7)] for _ in range(6)]
        self.game_over = False
        if starting_player is None:
            self.current_player = [player_1, player_2][randrange(2)]
        else:
            self.current_player = starting_player

    def play_one_turn(self):
        move = self.current_player.get_next_move(self.grid)
        self.make_move(move, self.current_player.tag)
        winner = self.get_winner()
        if winner:
            self.game_over = True
            self.winner_end(winner)
            return
        elif self.no_more_possible_moves():
            self.game_over = True
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


    def get_winner(self):
        if self.connect_4('X') >= 4:
            return 'X'
        if self.connect_4('O') >= 4:
            return 'O'
        return None


    def connect_4(self, tag, i_s=0, j_s=0, dir=None, acc_tags = 0):
        result = 0
        if dir is None:
            for i in range(i_s, 7):
                for j in range(j_s, 6):
                    if self.grid[j][i] == tag:
                        down_result = self.connect_4(tag, i, j, 'down', acc_tags + 1)
                        dl_result = self.connect_4(tag, i, j, 'down_left', acc_tags + 1)
                        dr_result = self.connect_4(tag, i, j, 'down_right', acc_tags + 1)
                        right_result = self.connect_4(tag, i, j, 'right', acc_tags + 1)
                        result = max(result, down_result, dr_result, dl_result, right_result)
            return result
        if dir == 'down':
            if j_s == 5 or self.grid[j_s + 1][i_s] != tag:
                return acc_tags
            return self.connect_4(tag, i_s, j_s + 1, 'down', acc_tags + 1)
        if dir == 'down_left':
            if j_s == 5 or i_s == 0 or self.grid[j_s + 1][i_s - 1] != tag:
                return acc_tags
            return self.connect_4(tag, i_s - 1, j_s + 1, 'down_left', acc_tags + 1)
        if dir == 'down_right':
            if j_s == 5 or i_s == 6 or self.grid[j_s + 1][i_s + 1] != tag:
                return acc_tags
            return self.connect_4(tag, i_s + 1, j_s + 1, 'down_right', acc_tags + 1)
        if dir == 'right':
            if i_s == 6 or self.grid[j_s][i_s + 1] != tag:
                return acc_tags
            return self.connect_4(tag, i_s + 1, j_s, 'right', acc_tags + 1)

