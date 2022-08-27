from tkinter import *

import barchart
import o_learns
from o_learns import feed_back_pro
import neural_lib as nl
from save_weights import *
import threading
import time


class Window:
    def __init__(self, game):
        self.root = Tk()
        self.game = game
        self.grid_vars = [[StringVar() for _ in range(7)] for _ in range(6)]
        self.game_stats_var = StringVar()
        self.back_prop_var = StringVar()
        self.target_var = StringVar()
        self.render_flag = True
        self.target_bars = []
        self.target_canvas = None
        self.best_move_toggle = False

        self.start()

    def start(self):
        self.root.bind("<KeyPress>", self.key_listener)
        self.render_grid()
        self.render_game_stats()
        self.render_target_bars()

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
                                f'Games won by {self.game.players[1]}: {self.game.games_won[self.game.players[1]]}\n'
                                f'Back propagation (b): {"On" if self.game.b_flag else "Off"}\n'
                                f'Best move (q): {"Active" if self.best_move_toggle else "Inactive"}\n'
                                f'Graphics (a): {"Active" if self.render_flag else "Inactive"}\n'
                                )

        label = Message(self.root, textvariable=self.game_stats_var, relief=RAISED, width=175)
        label.place(x=x_offset + 170, y=y_offset + 10)


    def update_game_stats(self):
        self.game_stats_var.set(f'Games played:      {self.game.games_played}\n'
                                f'Games won by {self.game.players[0]}: {self.game.games_won[self.game.players[0]]}\n'
                                f'Games won by {self.game.players[1]}: {self.game.games_won[self.game.players[1]]}\n'
                                f'Back propagation (b): {"On" if self.game.b_flag else "Off"}\n'
                                f'Best move (q): {"Active" if self.best_move_toggle else "Inactive"}\n'
                                f'Graphics (a): {"Active" if self.render_flag else "Inactive"}\n'
                                )

    def render_target_values(self, x_offset=20, y_offset=20):
        self.target_var.set(f'Targets:\n'
                            f'{nl.target[0]} {nl.target[1]} {nl.target[2]} {nl.target[3]} '
                            f'{nl.target[4]} {nl.target[5]} {nl.target[6]}')

        label = Message(self.root, textvariable=self.target_var, relief=RAISED, width=150)
        label.place(x=x_offset + 170, y=y_offset + 150)

    def render_target_bars(self):
        barchart.create(self.root, nl.out_layer.out)

    def update_target_values(self):
        self.target_var.set(f'Targets:\n'
                            f'{nl.target[0]} {nl.target[1]} {nl.target[2]} {nl.target[3]} '
                            f'{nl.target[4]} {nl.target[5]} {nl.target[6]}')

    def render_all(self):
        self.update_grid()
        self.render_target_bars()

    def erase(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def fun(self):
        while not self.game.space_flag:
            if not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    if self.game.b_flag:
                        feed_back_pro(self.game)
                i = -1
                if self.best_move_toggle:
                    i = self.get_best_move()
                self.game.play_one_turn(i)
                if self.game.current_player == self.game.players[0]:
                    o_learns.set_targets(self.game)
                time.sleep(0.02)

                if self.render_flag:
                    self.update_cell(self.game.last_move[0], self.game.last_move[1])
                    if self.game.current_player == self.game.players[0] and not self.game.game_over:
                        self.render_target_bars()
            else:
                self.game.restart()
                self.update_grid()
                self.update_game_stats()

    def get_best_move(self):
        if self.game.current_player == self.game.players[0]:
            return nl.net_winner
        return -1

    def key_listener(self, e):
        c = e.char

        if self.game.game_over and c in ['p', ' ', '0', '1', '2', '3', '4', '5', '6']:
            self.game.restart()
            self.update_game_stats()
            if self.render_flag:
                self.render_all()
        elif c == 'p':
            i = -1
            if self.best_move_toggle:
                i = self.get_best_move()
            if not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    if self.game.b_flag:
                        feed_back_pro(self.game)
                self.game.play_one_turn(i)
                if self.game.current_player == self.game.players[0]:
                    o_learns.set_targets(self.game)
                if self.render_flag:
                    self.update_cell(self.game.last_move[0], self.game.last_move[1])
                    if self.game.current_player == self.game.players[0] and not self.game.game_over:
                        self.render_target_bars()
        elif c == 'b':
            self.game.b_flag = not self.game.b_flag
            self.update_game_stats()

        elif c == ' ':
            self.game.space_flag = not self.game.space_flag

            if self.game.space_flag:
                t = threading.Thread(name = 'Verify space_flag', target=self.fun, args=())
                t.start()

            else:
                print('Stop')

        elif c in ['0', '1', '2', '3', '4', '5', '6']:
            if not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    if self.render_flag:
                        self.render_target_bars()
                self.game.play_one_turn(int(e.char))
                if self.render_flag:
                    self.update_cell(self.game.last_move[0], self.game.last_move[1])

        elif c == 'q':
            self.best_move_toggle = not self.best_move_toggle
            self.update_game_stats()

        elif c == 'a':
            self.render_flag = not self.render_flag
            self.update_game_stats()

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
            
            
            
