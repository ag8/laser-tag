import sys

import pygame
from pygame import gfxdraw

from Game import Game, Character
from utils import s

pygame.init()

game = Game()

scale = 80
black = 0, 0, 0
screen = pygame.display.set_mode((scale * 17, scale * 17))

team_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)

    for object in game.get_polygonal_items():
        vertices = object.get_position()

        scaled_vertices = s(vertices, scale)

        if type(object) is Character:
            pygame.gfxdraw.filled_polygon(screen, scaled_vertices, team_colors[object.team])
        else:
            pygame.gfxdraw.filled_polygon(screen, scaled_vertices, (200, 200, 200))
    game.step()
    pygame.display.flip()
