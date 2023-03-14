import math
import random

from alg import Algorithm


class Algorithm3(Algorithm):
    def __init__(self):
        super().__init__()

    def get_action(self, observation, reward):
        return math.floor(random.random() * 5)
