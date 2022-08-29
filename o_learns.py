import neural_lib as nl
from game import Game

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
    for i in range(6):
        k = moves_counter & (1 << i)
        nl.inputs[nl.GRID_SIZE * 3 + i] = 1.0 if (k > 0) else 0.0


def feed_back_pro(game: Game):
    search_for_max(game)
    nl.fix_all_weights()
    nl.backpropagation_count += 1


def feed_explorer():
    nl.gain = 0.5
    nl.calculate_hidden_layer()
    nl.gain = 1.5
    nl.calculate_output_layer()


def search_for_max(game: Game, gamma=0.75):
    grid = game.grid
    for i in range(7):
        if grid[0][i] == BLANK_CHAR:
            game.make_move(i, game.players[0])
            fill_inputs(game)
            feed_explorer()
            search_winner_neuron()
            nl.target[i] = nl.out_layer.out[nl.net_winner] * gamma
            winner = game.get_winner()
            if winner == game.players[0]:
                nl.target[i] = 1.0
            game.unmake_move(i)
        else:
            nl.target[i] = 0.0


def set_targets(game: Game, gamma=0.75):
    grid = game.grid
    for i in range(7):
        if grid[0][i] == BLANK_CHAR:
            game.make_move(i, game.players[0])
            winner = game.get_winner()
            if winner == game.players[0]:
                nl.target[i] = 1.0
            else:
                nl.target[i] = 0.0
            game.unmake_move(i)
        else:
            nl.target[i] = 0.0

