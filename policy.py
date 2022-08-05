from random import randrange


def get_next_move(grid: list[list[7]], i: int = -1):
    if i == -1:
        return get_random_move(grid)
    else:
        return get_human_move(grid, i)


def get_random_move(grid):
    while True:
        index = randrange(7)
        if grid[0][index] == '-':
            return index


def get_human_move(grid, i: int):
    if grid[0][i] == '-':
        return i
    else:
        print('The move you entered is invalid, doing some random move instead.')
        return get_random_move(grid)
