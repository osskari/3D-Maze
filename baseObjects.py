import random
from random import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *


class Drawable:
    def __init__(self, ambient, diffuse, specular, position, scale, shininess, offset):
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.position = position
        self.scale = scale
        self.shininess = shininess
        self.position_array = None
        self.normal_array = None
        self.offset = offset

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

    def set_color(self, shader):
        shader.set_material_ambient(*self.ambient)
        shader.set_material_diffuse(*self.diffuse)
        shader.set_material_specular(*self.specular)
        shader.set_material_shininess(self.shininess)

    def draw(self, model_matrix, shader):
        # set transformations
        model_matrix.add_translation(*self.position)
        model_matrix.add_scale(*self.scale)
        # set model matrix
        shader.set_model_matrix(model_matrix.matrix)


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
