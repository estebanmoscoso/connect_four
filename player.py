from policy import *


class Player:
    def __init__(self, tag: chr, policy_name='random'):
        self.tag = tag
        self.policy = Policy(policy_name)

    def get_next_move(self, grid: list[list[7]]):
        return self.policy.get_next_move(grid)

