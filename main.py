import math
import random
import sys

import numpy as np
import pygame
import tqdm as tqdm
from pygame import gfxdraw

import alg1
from Game import Game, Character
from alg2 import Algorithm2
from alg3 import Algorithm3
from alg4 import Algorithm4
from utils import s

pygame.init()

game = Game()

scale = 80
black = 0, 0, 0
screen = pygame.display.set_mode((scale * 17, scale * 17))
screen.unlock()

team_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
algorithms = [alg1.Algorithm1(), Algorithm2(), Algorithm3(), Algorithm4()]

observations, rewards = game.reset()

for i in tqdm.tqdm(range(100000000)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    for object in game.get_polygonal_items():
        vertices = object.get_vertices()

        scaled_vertices = s(vertices, scale)

        if type(object) is Character:
            pygame.gfxdraw.filled_polygon(screen, scaled_vertices, team_colors[object.team] if not object.intersecting else (255, 255, 255))
        else:
            pygame.gfxdraw.filled_polygon(screen, scaled_vertices, (200, 200, 200))



    character1 = game.get_polygonal_items()[0]
    sv = s(character1.get_vertices(), scale)
    # char1sub = screen.subsurface(max(sv[0][0] - 100, 0), max(sv[0][1] - 100, 0), 200, 200)
    # nice = pygame.surfarray.array3d(char1sub)
    # import matplotlib.image

    # matplotlib.image.imsave('name.png', nice)


    # rad = game.get_closest_objects()
    # pygame.gfxdraw.aacircle(screen, int(sv[0][0]), int(sv[0][1]), int(rad * scale), (200, 0, 0))

    # obs1 = game.get_observations()[0]
    # for obs in obs1:
    #     race, dist, angle = obs
    #
    #     v = sv[2] - sv[0]
    #
    #     u = np.matmul(np.array([[math.cos(angle), -math.sin(angle)],[math.sin(angle),math.cos(angle)]]), np.transpose(v))
    #     u = u / np.linalg.norm(u)
    #
    #     point = sv[0] + scale * dist * u
    #
    #     # print(point)
    #     pygame.gfxdraw.line(screen, int(sv[0][0]), int(sv[0][1]), int(point[0]), int(point[1]), (255, 255, 255) if race == 1 else (200, 0, 0))
    #
    #     # pygame.gfxdraw.aacircle(screen, int(point[0]), int(point[1]), int(50 * scale), (200, 0, 0))



    # print(obs1)

    actions = []
    for idx, character in enumerate(game.characters):
        actions.append(algorithms[character.team].get_action(observation=observations[idx], reward=rewards[idx]))

    observations, rewards = game.step([random.randint(0, 5) for i in range(8)])
    pygame.display.flip()
