import sys

import pygame
import tqdm as tqdm
from pygame import gfxdraw

from Game import Game, Character
from utils import s

pygame.init()

game = Game()

scale = 80
black = 0, 0, 0
screen = pygame.display.set_mode((scale * 17, scale * 17))
screen.unlock()

team_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]

for i in tqdm.tqdm(range(100000)):
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


    for point in game.get_eight_points():
        pygame.gfxdraw.filled_circle(screen, int(point[0] * scale), int(point[1] * scale), 10, (200, 0, 0))


    character1 = game.get_polygonal_items()[0]
    sv = s(character1.get_position(), scale)
    char1sub = screen.subsurface(max(sv[0][0] - 100, 0), max(sv[0][1] - 100, 0), 200, 200)
    nice = pygame.surfarray.array3d(char1sub)
    import matplotlib.image

    matplotlib.image.imsave('name.png', nice)

    game.step()
    pygame.display.flip()
