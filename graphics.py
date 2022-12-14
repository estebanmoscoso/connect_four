from tkinter import *

import barchart
import o_learns
from o_learns import feed_back_pro, fill_inputs
import neural_lib as nl
from save_weights import *
import threading
import time


class Window:
    def __init__(self, game):
        self.root = Tk()
        self.root.title("Connect Four")
        self.game = game
        self.grid_vars = [[StringVar() for _ in range(7)] for _ in range(6)]
        self.game_stats_var = StringVar()
        self.back_prop_var = StringVar()
        self.target_var = StringVar()
        self.render_flag = True
        self.target_bars = []
        self.target_canvas = None
        self.pesos_canvas = [[Canvas(width=4, height=4, bg="gray") for _ in range(60)] for _ in range(11)]
        self.neuronas_entrada_canvas = [Canvas(width=6, height=6, bg='gray') for _ in range(len(inputs)-6)]
        self.neuronas_escondidas_canvas = [Canvas(width=2, height=50, bg='deep pink') for _ in range(N_HID*2)]
        self.neuronas_salida_canvas = [Canvas(width=5, height=50, bg='blue violet') for _ in range(N_OUT*2)]
        self.best_move_toggle = False
        self.start()

    def start(self):
        self.root.bind("<KeyPress>", self.key_listener)
        self.render_grid()
        self.render_game_stats()
        self.render_target_bars()
        self.render_hidden_weights()
        self.render_input_neurons()
        self.render_hidden_neurons()
        self.render_out_neurons()

    def end(self):
        self.root.mainloop()

    
    def change_color_hidden_weights(self):
        for fila in range(len(self.pesos_canvas)):
            for columna in range(len(self.pesos_canvas[0])):
                if hidden_layer.weights[fila][columna] > 0.001:
                    self.pesos_canvas[fila][columna].configure(bg='red')
                elif hidden_layer.weights[fila][columna] < -0.001:
                    self.pesos_canvas[fila][columna].configure(bg='blue')
                else:
                    self.pesos_canvas[fila][columna].configure(bg='gray') 
                    
    def render_hidden_weights(self,x = 50, y = 300):
        c = 0
        for fila in range(len(self.pesos_canvas)):
            for columna in range(len(self.pesos_canvas[0])):
                c+=1
                self.pesos_canvas[fila][columna].place(x = x, y = y)
                x+= 6
            x = 50; y += 6    


    def change_input_neurons(self):
        for i in range(len(self.neuronas_entrada_canvas)):
            if inputs[i] == 1:
                self.neuronas_entrada_canvas[i].configure(bg='green') 
            else:
                self.neuronas_entrada_canvas[i].configure(bg='gray') 
                           
    def render_input_neurons(self,x = 30, y = 450):
        c = 0
        for i in range(len(self.neuronas_entrada_canvas)):
            self.neuronas_entrada_canvas[i].place(x = x, y = y)
            c+=1
            if c%3 == 0:
                x+=5
            x+=7
                           

    def render_hidden_neurons(self,x = 470, y = 310):
        for i in range(0,len(self.neuronas_entrada_canvas),2):
            self.neuronas_escondidas_canvas[i].place(x = x, y = y)
            #self.neuronas_escondidas_canvas[i].configure(bg='deep pink')
            self.neuronas_escondidas_canvas[i+1].place(x = x, y = y)
            self.neuronas_escondidas_canvas[i+1].configure(bg='light grey') 
            x+=4
                     
    def change_hidden_neurons(self):
        for i in range(N_HID):
            if hidden_layer.out[i] > 0:
                self.neuronas_escondidas_canvas[i*2+1].configure(height=50 - 50*hidden_layer.out[i])
            else:
                self.neuronas_escondidas_canvas[i*2+1].configure(height=50) 

    def change_color_hidden_neurons(self, color):
        for i in range(N_HID):
            self.neuronas_escondidas_canvas[i*2].configure(bg=color)



    def render_out_neurons(self,x = 480, y = 240):
        for i in range(0,len(self.neuronas_salida_canvas),2):
            self.neuronas_salida_canvas[i].place(x = x, y = y)
            #self.neuronas_salida_canvas[i].configure(bg='blue violet')
            self.neuronas_salida_canvas[i+1].place(x = x, y = y)
            self.neuronas_salida_canvas[i+1].configure(bg='light grey')
            x+=14

    def change_out_neurons(self):
        for i in range(N_OUT):
            if out_layer.out[i] > 0:
                self.neuronas_salida_canvas[i*2+1].configure(height=50 - 50*out_layer.out[i])
            else:
                self.neuronas_salida_canvas[i*2+1].configure(height=50)



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
        o_learns.fill_inputs(self.game)
        nl.calculate_hidden_layer()
        nl.calculate_output_layer()
        self.change_out_neurons()

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
        while self.game.space_flag:
            if not self.game.game_over:
                if self.game.current_player == self.game.players[0]:
                    if self.game.b_flag:
                        feed_back_pro(self.game)
                        if self.render_flag:
                            self.change_hidden_neurons()
                            self.change_color_hidden_weights()
                i = -1
                if self.best_move_toggle:
                    i = self.get_best_move()
                self.game.play_one_turn(i)
                fill_inputs(self.game)
                if self.render_flag:
                    self.change_input_neurons()
                
                if self.game.current_player == self.game.players[0]:
                    o_learns.set_targets(self.game)
                #time.sleep(0.02)

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
            o_learns.fill_inputs(self.game)
            nl.calculate_hidden_layer()
            nl.calculate_output_layer()
            o_learns.search_winner_neuron()
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
                
                fill_inputs(self.game)
                if self.render_flag:
                    self.change_input_neurons()
                if self.game.current_player == self.game.players[0]:
                    o_learns.set_targets(self.game)
                if self.render_flag:
                    self.update_cell(self.game.last_move[0], self.game.last_move[1])
                    if self.game.current_player == self.game.players[0] and not self.game.game_over:
                        self.render_target_bars()
        elif c == 'b':
            self.game.b_flag = not self.game.b_flag
            self.update_game_stats()
            if self.game.b_flag:
                if self.render_flag:
                    self.change_color_hidden_neurons('red')
            else:
                self.change_color_hidden_neurons('deep pink')

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
                fill_inputs(self.game)
                if self.render_flag:
                    self.change_input_neurons()
                
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
            if self.render_flag:
                self.change_color_hidden_weights()
            
        elif c == 'r':
            init_weights()
            if self.render_flag:
                self.change_color_hidden_weights()
            print('Pesos randomizados')
            
            

            
            
