from random import randrange


class Policy:
    def __init__(self, policy_name='random'):
        self.name = policy_name

    def get_next_move(self, grid: list[list[7]]):
        if self.name == 'random':
            return self.get_random_move(grid)
        if self.name == 'human':
            return self.get_human_move(grid)


    @staticmethod
    def get_random_move(grid):
        while True:
            index = randrange(7)
            if grid[0][index] == '-':
                return index

    @staticmethod
    def get_human_move(grid):
        # TODO
        return Policy.get_random_move(grid)
