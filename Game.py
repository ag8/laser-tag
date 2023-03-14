import math
import random
from abc import abstractmethod
from math import sin, cos, pi, inf

import numpy as np

CHARACTER = 0o0
WALL = 0o1


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


def is_point_inside_polygons(point, polygons):
    r = False

    for polygon in polygons:
        if is_point_inside_polygon(point, polygon.get_vertices()):
            return True

    return False


def get_direction_vector(theta):
    v = np.array([cos(theta), sin(theta)])
    return v / np.linalg.norm(v)


def closest_point(vertices, x0, y0):
    closest_points = []
    for i in range(len(vertices)):
        # Find the closest point on edge i to the given point
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % len(vertices)]
        dx = x2 - x1
        dy = y2 - y1
        t = ((x0 - x1) * dx + (y0 - y1) * dy) / (dx ** 2 + dy ** 2)
        if t <= 0:
            closest_points.append((x1, y1))
        elif t >= 1:
            closest_points.append((x2, y2))
        else:
            closest_points.append((x1 + t * dx, y1 + t * dy))

    # Calculate the distance between each closest point and the given point
    distances = [math.sqrt((x - x0) ** 2 + (y - y0) ** 2) for x, y in closest_points]

    # Choose the closest point
    closest_index = distances.index(min(distances))
    closest_x, closest_y = closest_points[closest_index]
    return np.array([closest_x, closest_y])


def filter_top(l, n):
    # Sort by distance
    sorted_list = sorted(l, key=lambda x: x[1])

    # Return closest ten
    return sorted_list[:n]


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_angle(v0, v1):
    return np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))


class GameObject:
    def __init__(self):
        pass

    @abstractmethod
    def get_vertices(self):
        pass

    @abstractmethod
    def get_closest_point_to(self, point):
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

        self.type = CHARACTER

    def dir_v(self):
        return get_direction_vector(self.direction)

    def get_vertices(self):
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

    def get_pos(self):
        return np.array(self.coords)

    def get_closest_point_to(self, point):
        return closest_point(self.get_vertices(), point[0], point[1])


class Wall(GameObject):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.type = WALL

    def get_vertices(self):
        return (self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2), (self.x1, self.y2)

    def get_closest_point_to(self, point):
        return closest_point(self.get_vertices(), point[0], point[1])


class Game:
    num_teams = 4
    characters_per_team = 2

    def __init__(self):
        # Create characters
        self.characters = []

        for i in range(Game.num_teams):
            for j in range(Game.characters_per_team):
                self.characters.append(Character(random.random() * 17, random.random() * 17, i))

        with open('layout.txt') as file:
            lines = [line.rstrip() for line in file]

        self.walls = []
        for i in range(len(lines)):
            for j in range(len(lines[0])):
                if lines[i][j] == 'X':
                    self.walls.append(Wall(i, j, i + 1, j + 1))

    def get_polygonal_items(self, ignore=None):
        s = []
        s.extend(self.characters)
        s.extend(self.walls)
        if ignore in s:
            s.remove(ignore)
        return s

    def get_closest_objects(self):
        character = self.characters[0]

        closest_distance = inf
        loc = character.get_vertices()[0]

        for other_character in self.characters:
            if other_character == character:
                continue

            oloc = other_character.get_vertices()[0]

            dist = math.sqrt((loc[0] - oloc[0]) ** 2 + (loc[1] - oloc[1]) ** 2)

            if dist < closest_distance:
                closest_distance = dist

        return closest_distance

    def get_observation(self, character):
        # Get distances to all objects
        object_distances = []

        for object in self.get_polygonal_items():
            closest = object.get_closest_point_to(character.get_pos())
            distance = dist(closest, character.get_pos())
            vector_to_closest = closest - character.get_pos()
            vector_pointing = character.get_vertices()[2] - character.get_vertices()[0]
            angle = get_angle(vector_pointing, vector_to_closest)

            object_distances.append([object.type, distance, angle])

        object_distances = filter_top(object_distances, 10)
        return object_distances

    def get_observations(self):
        observations = []

        for character in self.characters:
            observations.append(self.get_observation(character))

        # print(observations)
        return observations

    def step(self, actions):
        rewards = np.zeros(len(self.characters), dtype=int)

        for idx, character in enumerate(self.characters):
            if actions[idx] == 0:  # do nothing
                pass
            elif actions[idx] == 1:  # accelerate
                character.velocity += 0.001
            elif actions[idx] == 2:  # slow down
                if character.velocity > 0:
                    character.velocity -= 0.001
            elif actions[idx] == 3:  # rotate right
                character.direction += pi / 100
            elif actions[idx] == 4:  # rotate left
                character.direction -= pi / 100
            elif actions[idx] == 5:  # shoot
                pass

            # Move characters
            character.coords += character.dir_v() * character.velocity
            cnc = character.get_vertices()[2]

            # Detect intersections
            intersection = False

            # Boundaries
            if character.coords[0] != max(0, min(17, character.coords[0])) or \
                    character.coords[1] != max(0, min(17, character.coords[1])):
                intersection = True

            if cnc[0] != max(0, min(17, cnc[0])) or cnc[1] != max(0, min(17, cnc[1])):
                intersection = True

            # Other characters
            for other_object in self.get_polygonal_items():
                if other_object == character:
                    continue

                if is_point_inside_polygon(character.get_vertices()[2], list(other_object.get_vertices())):
                    intersection = True

            if intersection:
                character.direction = character.direction + pi
                rewards[idx] -= 10  # crashing into things is bad

        return self.get_observations(), rewards
