import random
from abc import abstractmethod
from math import sin, cos, pi

import numpy as np


def is_point_inside_polygon(point, polygon):
    """
    Determines if a given point is inside a convex polygon.

    :param point: A tuple representing the (x, y) coordinates of the point.
    :param polygon: A list of tuples representing the vertices of the polygon.
                    The vertices should be listed in clockwise or counterclockwise order.
    :return: True if the point lies inside the polygon, False otherwise.
    """
    x, y = point
    n = len(polygon)
    inside = False

    # Iterate over each edge of the polygon
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]

        # Check if the point is within the y-bounds of the edge
        if (p1y < y <= p2y) or (p2y < y <= p1y):
            # Calculate the x-coordinate of the intersection of the edge and a horizontal line passing through the point
            x_intersect = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

            # If the point is to the left of the intersection, toggle the inside flag
            if x <= x_intersect:
                inside = not inside

        p1x, p1y = p2x, p2y

    return inside


def get_direction_vector(theta):
    v = np.array([cos(theta), sin(theta)])
    return v / np.linalg.norm(v)


class GameObject:
    def __init__(self):
        pass

    @abstractmethod
    def get_position(self):
        pass


class Character(GameObject):
    def __init__(self, x, y, team):
        super().__init__()
        self.coords = np.array([x, y])
        self.direction = random.random() * 2 * pi
        self.team = team

        self.action = 0  # start off doing nothing

        self.velocity = 0.01

        self.ammo = 1000

    def dir_v(self):
        return get_direction_vector(self.direction)

    def get_position(self):
        # First coordinate is (x, y)
        first_coord = np.array(self.coords, dtype=np.float64)

        # Third coordinate is tip of nose
        dir_vector = get_direction_vector(self.direction)
        third_coord = first_coord + dir_vector * 0.4

        # Second coordinate is left bottom corner
        perp = np.array([-dir_vector[1], dir_vector[0]])
        second_coord = first_coord + perp * 0.1

        # Fourth coordinatre is right bottom orner
        fourth_coord = first_coord - perp * 0.1

        return first_coord, second_coord, third_coord, fourth_coord


class Wall(GameObject):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_position(self):
        return (self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2)


class Game:
    num_teams = 4
    characters_per_team = 4

    def __init__(self):
        # Create characters
        self.characters = []

        for i in range(Game.num_teams):
            for j in range(Game.characters_per_team):
                self.characters.append(Character(random.random() * 16, random.random() * 16, i))

        with open('layout.txt') as file:
            lines = [line.rstrip() for line in file]

        self.walls = []
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == 'X':
                    self.walls.append(Wall(i, j, i + 1, j + 1))

    def get_polygonal_items(self):
        s = []
        s.extend(self.characters)
        s.extend(self.walls)
        return s

    def step(self):
        for character in self.characters:
            character.coords += character.dir_v() * character.velocity
            character.direction += pi / 1000

            # Detect intersections
            intersection = False

            # Boundaries
            if character.coords[0] != max(0, min(16, character.coords[0])) or \
                    character.coords[1] != max(0, min(16, character.coords[1])):
                intersection = True

            # Other characters
            for other_object in self.get_polygonal_items():
                if other_object == character:
                    continue

                if is_point_inside_polygon(character.get_position()[2], list(other_object.get_position())):
                    intersection = True

            if intersection:
                character.direction = character.direction + pi
