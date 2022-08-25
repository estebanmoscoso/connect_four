from tkinter import *

import o_learns
from o_learns import feed_back_pro
import neural_lib as nl
from save_weights import *

class Window:
    def __init__(self, game):
        self.root = Tk()
        self.game = game
        self.grid_vars = [[StringVar() for _ in range(7)] for _ in range(6)]
        self.game_stats_var = StringVar()
        self.back_prop_var = StringVar()
        self.target_var = StringVar()

        self.start()

    def start(self):
        self.root.bind("<KeyPress>", self.key_listener)
        self.render_grid()
        self.render_game_stats()
        self.render_back_propagation()
        self.render_target_values()

    def end(self):
        self.root.mainloop()

    def render_grid(self, x_offset=20, y_offset=20):
        grid = self.game.grid
        for i in range(8):
            vertical_line = Frame(self.root, bg='white', height=152, width=1)
            vertical_line.place(x=x_offset + 20 * i, y=y_offset)
        for i in range(6):
            horizontal_line = Frame(self.root, bg='white', height=1, width=140)
            horizontal_line.place(x=x_offset, y=y_offset + 26 + 25 * i)

        for j in range(6):
            for i in range(7):
                self.grid_vars[j][i].set(grid[j][i])
                label = Label(self.root, textvariable=self.grid_vars[j][i])
                label.place(x=3 + x_offset + 20 * i, y=2 + y_offset + 25 * j)

        for i in range(7):
            label = Label(self.root, text=str(i))
            label.place(x=3 + x_offset + 20 * i, y=2 + y_offset + 25 * 6)

    def update_cell(self, i, j):
        self.grid_vars[j][i].set(self.game.grid[j][i])

    def update_grid(self):
        for j in range(6):
            for i in range(7):
                self.update_cell(i, j)

    def render_game_stats(self, x_offset=20, y_offset=20):
        self.game_stats_var.set(f'Games played:      {self.game.games_played}\n'
                                f'Games won by {self.game.players[0]}: {self.game.games_won[self.game.players[0]]}\n'
                                f'Games won by {self.game.players[1]}: {self.game.games_won[self.game.players[1]]}')

        label = Message(self.root, textvariable=self.game_stats_var, relief=RAISED, width=150)
        label.place(x=x_offset + 170, y=y_offset + 10)

    def render_back_propagation(self, x_offset=20, y_offset=20):
        self.back_prop_var.set(f'Back propagation: {"On" if self.game.b_flag else "Off"}')
        label = Message(self.root, textvariable=self.back_prop_var, relief=RAISED, width=150)
        label.place(x=x_offset + 170, y=y_offset + 110)

    def update_back_propagation(self):
        self.back_prop_var.set(f'Back propagation: {"On" if self.game.b_flag else "Off"}')

    def update_game_stats(self):
        self.game_stats_var.set(f'Games played:      {self.game.games_played}\n'
                                f'Games won by {self.game.players[0]}: {self.game.games_won[self.game.players[0]]}\n'
                                f'Games won by {self.game.players[1]}: {self.game.games_won[self.game.players[1]]}')

    def render_target_values(self, x_offset=20, y_offset=20):
        self.target_var.set(f'Targets:\n'
                            f'{nl.target[0]} {nl.target[1]} {nl.target[2]} {nl.target[3]} '
                            f'{nl.target[4]} {nl.target[5]} {nl.target[6]}')

        label = Message(self.root, textvariable=self.target_var, relief=RAISED, width=150)
        label.place(x=x_offset + 170, y=y_offset + 150)

    def update_target_values(self):
        self.target_var.set(f'Targets:\n'
                            f'{nl.target[0]} {nl.target[1]} {nl.target[2]} {nl.target[3]} '
                            f'{nl.target[4]} {nl.target[5]} {nl.target[6]}')

    def erase(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def key_listener(self, e):
        c = e.char

        if self.game.game_over and c in ['p', ' ', '0', '1', '2', '3', '4', '5', '6']:
            self.game.restart()
            self.update_grid()
            self.update_game_stats()
            self.update_target_values()
        elif c == 'p':
            if not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    feed_back_pro(self.game)
                    self.update_target_values()
                self.game.play_one_turn(-1)
                self.update_cell(self.game.last_move[0], self.game.last_move[1])
        elif c == 'b':
            self.game.b_flag = not self.game.b_flag
            self.update_back_propagation()

        elif c == ' ':
            while not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    feed_back_pro(self.game)
                    self.update_target_values()
                self.game.play_one_turn(-1)
                self.update_cell(self.game.last_move[0], self.game.last_move[1])

        elif c in ['0', '1', '2', '3', '4', '5', '6']:
            if not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    feed_back_pro(self.game)
                    self.update_target_values()
                self.game.play_one_turn(int(e.char))
                self.update_cell(self.game.last_move[0], self.game.last_move[1])

        elif c == 'q':
            if not self.game.game_over:
                i = -1
                if self.game.current_player == self.game.players[0]:
                    i = o_learns.search_for_max(self.game)
                    # print('best move: ', i)
                self.game.play_one_turn(i)
                self.update_cell(self.game.last_move[0], self.game.last_move[1])

        elif c == 'x':
            self.root.destroy()
            
        elif c == 's':
            salvar_pesos()
            print('Pesos Guardados')
            
        elif c == 'c':
            cargar_pesos()
            print('Pesos Cargados')
            
        elif c == 'r':
            init_weights()
            print('Pesos randomizados')
            print(nl.hidden_layer.weights)
            print(nl.out_layer.weights)
            
            
            
