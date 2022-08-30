import neural_lib as nl
from game import Game
import time
BLANK_CHAR = ' '


def search_winner_neuron():
    nl.net_winner = 0
    nl.peak_value = 0
    for i in range(nl.N_OUT):
        if nl.out_layer.out[i] >= nl.peak_value:
            nl.peak_value = nl.out_layer.out[i]
            nl.net_winner = i


def fill_inputs(game: Game):
    grid = game.grid
    moves_counter = game.moves_counter
    for j in range(7):
        for k in range(6):
            i = 3*(7*k+j)
            if grid[k][j] == 'O':
                nl.inputs[i] = 0
                nl.inputs[i+1] = 0
                nl.inputs[i+2] = 1
            if grid[k][j] == BLANK_CHAR:
                nl.inputs[i] = 0
                nl.inputs[i+1] = 1
                nl.inputs[i+2] = 0
            if grid[k][j] == 'X':
                nl.inputs[i] = 1
                nl.inputs[i+1] = 0
                nl.inputs[i+2] = 0

def feed_back_pro(game: Game):
    search_for_max(game)
    nl.fix_all_weights()
    nl.backpropagation_count += 1


def feed_explorer():
    nl.calculate_hidden_layer()
    nl.calculate_output_layer()


def search_for_max(game: Game):
    # grid = game.grid
    # for i in range(7):
    #     if grid[0][i] == BLANK_CHAR:
    #         game.make_move(i, game.players[0])
    #         winner = game.get_winner()
    #         game.unmake_move(i)
    #         if winner == game.players[0]:
    #             #game.unmake_move(i)
    #             for j in range(nl.N_OUT):
    #                 nl.target[j] = 0.0
    #             nl.target[i] = 1.0
    #             print(nl.target)
    #             print(game.grid)
    #             fill_inputs(game)
    #             feed_explorer()
    #             nl.target[i] = 0.0
    grid = game.grid
    for i in range(7):
        if grid[0][i] == BLANK_CHAR:
            game.make_move(i, game.players[0])
            winner = game.get_winner()
            game.unmake_move(i)
            if winner == game.players[0]:
                print(f'Winner position in column {i}.')
                #game.unmake_move(i)
                for j in range(nl.N_OUT):
                    nl.target[j] = 0.0
                nl.target[i] = 1.0
                print("\n1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1")
                print(nl.target)
                #print(game.grid)
                fill_inputs(game)
                
                
                for j in range(len(nl.inputs)):
                    if j%21 == 0:
                        print('\n')
                    if (j+1)%3 == 0:
                        print(nl.inputs[j], end = ' ')
                    else:
                        print(nl.inputs[j], end = '') 
                
                
                
                
                print('-------------------------------------------------------------')
                feed_explorer()
                nl.target[i] = 0.0
                #time.sleep(4)

def set_targets(game: Game):
    # grid = game.grid
    # for i in range(7):
    #     if grid[0][i] == BLANK_CHAR:
    #         game.make_move(i, game.players[0])
    #         winner = game.get_winner()
    #         if winner == game.players[0]:
    #             nl.target[i] = 1.0
    #         else:
    #             nl.target[i] = 0.0
    #         game.unmake_move(i)
    #     else:
    #         nl.target[i] = 0.0
    # grid = game.grid
    # for i in range(7):
    #     if grid[0][i] == BLANK_CHAR:
    #         game.make_move(i, game.players[0])
    #         winner = game.get_winner()
    #         game.unmake_move(i)
    #         if winner == game.players[0]:
    #             #game.unmake_move(i)
    #             for j in range(nl.N_OUT):
    #                 nl.target[j] = 0.0
    #             nl.target[i] = 1.0
    #             print("\n2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")
    #             print(nl.target)
    #             print(game.grid)
    #             fill_inputs(game)
    #             # for j in range(len(nl.inputs)):
    #             #     if j%21 == 0:
    #             #         print('\n')
    #             #     if (j+1)%3 == 0:
    #             #         print(nl.inputs[j], end = ' ')
    #             #     else:
    #             #         print(nl.inputs[j], end = '') 
    #             print("\n###############################################")
    #             feed_explorer()
    #             nl.target[i] = 0.0
                
    #             #time.sleep(4)

    pass