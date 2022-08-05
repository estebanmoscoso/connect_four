import neural_lib as nl
from game import Game

BP_COUNT = 0  # TODO: search where does this value come from
NET_WINNER = 0
GAMMA = 0.1  # TODO: search where does this value come from

def search_winner_neuron():
    global NET_WINNER
    NET_WINNER = 0  # TODO: search where does this value come from
    peak_value = nl.counselor_out.out[0]  # TODO: search where does this value come from
    for i in range(nl.N_OUT):
        nl.counselor_out[i] = 0.0
        if nl.out_layer.out[i] >= peak_value:
            peak_value = nl.out_layer.out[i]
            NET_WINNER = i


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
            if grid[k][j] == '-':
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


def feed_back_pro():
    global BP_COUNT
    nl.gain = 0.5
    nl.calculate_hidden_layer()
    nl.gain = 1.5
    nl.calculate_output_layer()

    b_flag = True  # TODO: search where does this value come from
    if b_flag:
        nl.fix_all_weights()
        BP_COUNT += 1


def feed_explorer():
    nl.gain = 0.5
    nl.calculate_hidden_layer()
    nl.gain = 1.5
    nl.calculate_output_layer()


def search_for_max(game: Game):
    global NET_WINNER, GAMMA
    grid = game.grid
    for i in range(7):
        if grid[0][i] == '-':
            game.make_move(i, game.players[0])
            fill_inputs(game)
            feed_explorer()
            search_winner_neuron()
            nl.target[NET_WINNER] = nl.out_layer[NET_WINNER] * GAMMA
            winner = game.get_winner()
            if winner == game.players[0]:
                nl.target[i] = 1.0
            # plot_targets()
            game.unmake_move(i)
