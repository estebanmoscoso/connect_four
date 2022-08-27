from random import randrange
from policy import get_next_move
import neural_lib as nl
BLANK_CHAR = ' '


class Game:
    def __init__(self, player_1: str = 'X', player_2: str = 'O', starting_player = None):
        self.players = [player_1, player_2]
        self.starting_player = starting_player
        self.grid = [[BLANK_CHAR for _ in range(7)] for _ in range(6)]
        self.game_over = False
        self.games_played = 0
        self.games_won = {player_1: 0, player_2: 0}
        self.last_move = (-1, -1)
        self.moves_counter = 0
        self.b_flag = False

        if starting_player is None:
            self.current_player = [player_1, player_2][randrange(2)]
        else:
            self.current_player = starting_player

    def restart(self):
        self.grid = [[BLANK_CHAR for _ in range(7)] for _ in range(6)]
        self.game_over = False
        self.moves_counter = 0
        for i in range(7):
            nl.target[i] = 0.0

        if self.starting_player is None:
            self.current_player = self.players[randrange(2)]
        else:
            self.current_player = self.starting_player

    def play_one_turn(self, index=-1):
        #En caso de se juegue en la ultima fila
        move = get_next_move(self.grid, index) #Retorna el indice de la columna donde se va a jugar en la ultima fila
        self.save_last_move(move) #Guarda la (columna, fila) donde se realiza el ultimo movimiento permitido
        self.make_move(move, self.current_player)
        winner = self.get_winner()
        if winner:
            self.game_over = True
            self.games_played += 1
            self.games_won[winner] += 1
            self.winner_end(winner)
            return
        elif self.no_more_possible_moves():
            self.game_over = True
            self.games_played += 1
            self.tie_end()
            return
        self.change_player()
        self.moves_counter += 1

    def change_player(self):
        if self.current_player == self.players[0]:
            self.current_player = self.players[1]
        else:
            self.current_player = self.players[0]

    def no_more_possible_moves(self):
        return all([self.grid[0][i] != BLANK_CHAR for i in range(7)])

    @staticmethod
    def winner_end(winner):
        print('Game is over!', winner, 'wins!')

    @staticmethod
    def tie_end():
        print('Game is over! There are no more possible moves!')

    def make_move(self, move, tag):  #tag es self 'X' u 'O'
        for i in range(5, -1, -1): #Va de la fila 5 a 0
            if self.grid[i][move] == BLANK_CHAR:
                self.grid[i][move] = tag
                return

    def unmake_move(self, move):
        for i in range(6):
            if self.grid[i][move] != BLANK_CHAR:
                self.grid[i][move] = BLANK_CHAR
                return

    def save_last_move(self, move):  #Explora las filas de 0 a 5 en busqueda de la fila con espacio en blanco donde jugar.
        for i in range(5): #i posible fila donde jugar, i+1 fila a analizar para saber si ya se ha jugado ahi (tiene X u O)
            if self.grid[i+1][move] != BLANK_CHAR:
                self.last_move = (move, i)
                return
        self.last_move = (move, 5) #Si de 0 a 4 no hay una fila vacia, entonces juega en la 5

    def get_winner(self):
        for player in self.players:
            if self.check_connect_4(player) >= 4:
                return player
        return None

    def check_connect_4(self, tag, i_s=0, j_s=0, direction=None, acc_tags=0):
        result = 0
        if direction is None:
            for i in range(i_s, 7):
                for j in range(j_s, 6):
                    if self.grid[j][i] == tag:
                        down_result = self.check_connect_4(tag, i, j, 'down', acc_tags + 1)
                        dl_result = self.check_connect_4(tag, i, j, 'down_left', acc_tags + 1)
                        dr_result = self.check_connect_4(tag, i, j, 'down_right', acc_tags + 1)
                        right_result = self.check_connect_4(tag, i, j, 'right', acc_tags + 1)
                        result = max(result, down_result, dr_result, dl_result, right_result)
            return result
        if direction == 'down':
            if j_s == 5 or self.grid[j_s + 1][i_s] != tag:
                return acc_tags
            return self.check_connect_4(tag, i_s, j_s + 1, 'down', acc_tags + 1)
        if direction == 'down_left':
            if j_s == 5 or i_s == 0 or self.grid[j_s + 1][i_s - 1] != tag:
                return acc_tags
            return self.check_connect_4(tag, i_s - 1, j_s + 1, 'down_left', acc_tags + 1)
        if direction == 'down_right':
            if j_s == 5 or i_s == 6 or self.grid[j_s + 1][i_s + 1] != tag:
                return acc_tags
            return self.check_connect_4(tag, i_s + 1, j_s + 1, 'down_right', acc_tags + 1)
        if direction == 'right':
            if i_s == 6 or self.grid[j_s][i_s + 1] != tag:
                return acc_tags
            return self.check_connect_4(tag, i_s + 1, j_s, 'right', acc_tags + 1)
