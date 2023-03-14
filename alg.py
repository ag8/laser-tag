from abc import abstractmethod


class Algorithm:
    def __init__(self):
        pass

    @abstractmethod
    def get_action(self, observation, reward):
        pass

