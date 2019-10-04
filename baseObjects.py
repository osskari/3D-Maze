import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

# from gameObjects import Drawable


class Drawable:
    def __init__(self, diffuse, specular, position, scale, shininess):
        self.diffuse = diffuse
        self.specular = specular
        self.position = position
        self.scale = scale
        self.shininess = shininess


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.z > other.z

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.z < other.z

    def __iter__(self):
        return (self.__getitem__(x) for x in range(3))

    def __getitem__(self, item):
        if item == 0 or item == "X":
            return self.x
        if item == 1 or item == "Y":
            return self.y
        if item == 2 or item == "Z":
            return self.z


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)


class Cube(Drawable):
    def __init__(self, diffuse, specular, position, scale, shininess):
        Drawable.__init__(self, diffuse, specular, position, scale, shininess)
        self.position_array = [-0.5, -0.5, -0.5,
                               -0.5, 0.5, -0.5,
                               0.5, 0.5, -0.5,
                               0.5, -0.5, -0.5,
                               -0.5, -0.5, 0.5,
                               -0.5, 0.5, 0.5,
                               0.5, 0.5, 0.5,
                               0.5, -0.5, 0.5,
                               -0.5, -0.5, -0.5,
                               0.5, -0.5, -0.5,
                               0.5, -0.5, 0.5,
                               -0.5, -0.5, 0.5,
                               -0.5, 0.5, -0.5,
                               0.5, 0.5, -0.5,
                               0.5, 0.5, 0.5,
                               -0.5, 0.5, 0.5,
                               -0.5, -0.5, -0.5,
                               -0.5, -0.5, 0.5,
                               -0.5, 0.5, 0.5,
                               -0.5, 0.5, -0.5,
                               0.5, -0.5, -0.5,
                               0.5, -0.5, 0.5,
                               0.5, 0.5, 0.5,
                               0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, -1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, 0.0, 1.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, -1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             0.0, 1.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             -1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0,
                             1.0, 0.0, 0.0]

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

    def set_color(self, shader):
        shader.set_material_diffuse(*self.diffuse)
        shader.set_material_specular(*self.specular)
        shader.set_material_shininess(self.shininess)

    def draw(self, model_matrix, shader):
        # set transformations
        model_matrix.add_translation(*self.position)
        model_matrix.add_scale(*self.scale)
        # set model matrix
        shader.set_model_matrix(model_matrix.matrix)
        # draw
        for i in range(0, 21, 4):
            glDrawArrays(GL_TRIANGLE_FAN, i, 4)


class Sphere:
    def __init__(self, stacks=12, slices=24):
        self.vertex_array = []
        self.slices = slices

        stack_interval = pi/stacks
        slice_interval = 2.0*pi/slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                self.vertex_array.append(sin(stack_angle) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle))
                self.vertex_array.append(sin(stack_angle) * sin(slice_angle))

                self.vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle + stack_interval))
                self.vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                self.vertex_count += 2

    def set_vertices(self, shader):
        shader.set_position_attribute(self.vertex_array)
        shader.set_normal_attribute(self.vertex_array)

    def draw(self):
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)


class Game:
    def __init__(self, shader, model_matrix, view_matrix, projection_matrix, player):
        self.shader = shader
        shader.use()
        self.model_matrix = model_matrix
        self.view_matrix = view_matrix
        self.player = player
        self.look()
        self.projection_matrix = projection_matrix

    def look(self):
        self.view_matrix.look(self.player.position, self.player.looking_at, self.player.normal)

    def set_perspective(self, fov, aspect, near, far):
        self.projection_matrix.set_perspective(fov, aspect, near, far)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())


class Player:
    def __init__(self, position, speed, rotation_speed, looking_at):
        self.position = position
        self.speed = speed
        self.rotationSpeed = rotation_speed
        self.looking_at = Point(looking_at.x, self.position.y, looking_at.z)
        self.normal = Vector(0, 1, 0)


class Rectangle(Drawable):
    def __init__(self, color, position, scale):
        Drawable.__init__(self, color, position, scale, (1,1,1), 13)

    def draw(self, model_matrix, shader, cube):
        # shader.set_solid_color(*self.color)
        model_matrix.add_translation(*self.position)
        # model_matrix.push_matrix()
        model_matrix.add_scale(*self.scale)
        shader.set_model_matrix(model_matrix.matrix)
        cube.draw()
        # model_matrix.pop_matrix()


class Maze:
    def __init__(self):
        self.walls = []
        self.lights = []


class Level:
    def __init__(self, floor, maze):
        self.floor = floor
        self.maze = maze

    def collision(self, new_pos, offset, matrix):
        for wall in self.maze.walls:
            if matrix.is_between(new_pos, wall, offset):
                return wall
        return None


class Light:
    def __init__(self, position, diffuse, specular=None):
        self.position = position
        self.diffuse = diffuse
        self.specular = specular if specular else diffuse


inputs = {
            "W": False,  # Walk forward
            "A": False,  # Turn left
            "S": False,  # Walk backwards
            "D": False   # Turn right
        }