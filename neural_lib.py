from random import randrange
from math import exp
ROWS = 6
COLUMNS = 7
GRID_SIZE = ROWS*COLUMNS
N_MOVES = 6
N_IN = GRID_SIZE*3 + N_MOVES
N_OUT = COLUMNS
N_HID = (N_IN + N_OUT)//2  # TO DO: Get a more appropriate value

mid = 0.5
eta = 0.125
gain = 1.5
alpha = 0.5
target = [0 for _ in range(N_OUT)]
counselor_out = [0 for _ in range(N_OUT)]
inputs = [0 for _ in range(N_IN)]
peak_value = 0
net_winner = 0
backpropagation_count = 0


class OutLayer:
    def __init__(self):
        self.weights = [[0 for _ in range(N_HID)] for _ in range(N_OUT)]
        self.error = [0 for _ in range(N_OUT)]
        self.moment = [[0 for _ in range(N_HID)] for _ in range(N_OUT)]
        self.out = [0 for _ in range(N_OUT)]


class HiddenLayer:
    def __init__(self):
        self.weights = [[0 for _ in range(N_IN)] for _ in range(N_HID)]
        self.error = [0 for _ in range(N_HID)]
        self.moment = [[0 for _ in range(N_IN)] for _ in range(N_HID)]
        self.out = [0 for _ in range(N_HID)]


out_layer = OutLayer()
hidden_layer = HiddenLayer()


def get_random_weight():
    return randrange(-50, 51)/100


def init_weights():
    for k in range(N_HID):
        for i in range(N_IN):
            hidden_layer.weights[k][i] = get_random_weight()
        
    for k in range(N_OUT):
        for i in range(N_HID):
            out_layer.weights[k][i] = get_random_weight()


def clear_weights():
    for k in range(N_HID):
        for i in range(N_IN):
            hidden_layer.weights[k][i] = 0


def fix_all_weights():
    # Output layer error
    for k in range(N_OUT):
        out_layer.error[k] = out_layer.out[k] * (1 - out_layer.out[k]) * (target[k] - out_layer.out[k])

    # Hidden layer error
    for k in range(N_HID):
        s = 0
        for i in range(N_OUT):
            s += out_layer.error[i] + out_layer.weights[i][k]
        hidden_layer.error[k] = hidden_layer.out[k] * (1-hidden_layer.out[k]) * s

    # Fixing weights of output layer
    for k in range(N_OUT):
        for i in range(N_HID):
            delta = eta * out_layer.error[k] * hidden_layer.out[i]
            out_layer.weights[k][i] = hidden_layer.weights[k][i] + delta + (alpha * hidden_layer.moment[k][i])

    # Fixing weights of hidden layer
    for k in range(N_HID):
        for i in range(N_IN):
            delta = eta * hidden_layer.error[k] * inputs[i]
            hidden_layer.weights[k][i] = hidden_layer.weights[k][i] + delta + (alpha * hidden_layer.moment[k][i])
            hidden_layer.moment[k][i] = delta


def sigmoid(x: float):
    out = 1/(1 + exp(-gain * x))
    return out


def calculate_hidden_layer():
    for k in range(N_HID):
        hidden_layer.out[k] = 0
        for i in range(N_IN):
            hidden_layer.out[k] += hidden_layer.weights[k][i] * inputs[i]
        hidden_layer.out[k] = sigmoid(hidden_layer.out[k])


def calculate_output_layer():
    for k in range(N_OUT):
        out_layer.out[k] = 0
        if inputs[3*k+1] == 1:
            for i in range(N_HID):
                out_layer.out[k] += out_layer.weights[k][i] * hidden_layer.out[i]
            out_layer.out[k] = sigmoid(out_layer.out[k])


def inject_noise_weights():
    # Noise injection for hidden layer
    for k in range(N_HID):
        for i in range(N_IN):
            dice = randrange(10)
            if dice == 0:
                tmp = randrange(-50, 51)
                tmp = tmp // 100
                hidden_layer.weights[k][i] = tmp

    # Noise injection for output layer
    for k in range(N_OUT):
        for i in range(N_HID):
            dice = randrange(10)
            if dice == 0:
                tmp = randrange(-50, 51)
                tmp = tmp // 100
                out_layer.weights[k][i] = tmp
