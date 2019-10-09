from math import *


# Contains base variables and methods that any drawable needs to implement
class Drawable:
    def __init__(self, ambient, diffuse, specular, position, scale, shininess, offset):
        self.ambient = ambient  # Ambient color values of drawable
        self.diffuse = diffuse  # Diffuse color values of drawable
        self.specular = specular  # Specular color values of drawable
        self.position = position  # Position of drawable
        self.scale = scale  # Drawable scale on each axis
        self.shininess = shininess  # Shininess of object
        self.position_array = None  # Array of points to draw
        self.normal_array = None  # Normals for surfaces on object
        self.offset = offset  # Collision buffer around object for clipping

    # Sends positions and normals to the shader
    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)

    # Sends all color values and shininess to shader
    def set_color(self, shader):
        shader.set_material_ambient(*self.ambient)
        shader.set_material_diffuse(*self.diffuse)
        shader.set_material_specular(*self.specular)
        shader.set_material_shininess(self.shininess)

    # Base transformations needed each draw
    def draw(self, model_matrix, shader):
        # set transformations
        model_matrix.add_translation(*self.position)
        model_matrix.add_scale(*self.scale)
        # set model matrix
        shader.set_model_matrix(model_matrix.matrix)


# A point in 3 dimensional space
class Point:
    def __init__(self, x, y, z):
        self.x = x  # Place on x-axis
        self.y = y  # Place on y-axis
        self.z = z  # Place on z-axis

    # Add two points to get a new point
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    # Get vector between two points
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    # Stringify each coordinate, mainly used for debugging
    def __str__(self):
        return "x: " + str(self.x) + ", y: " + str(self.y) + ", z: " + str(self.z)

    # Determine if two objects are in the same spot
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # Determine if Point is larger than another Point
    def __gt__(self, other):
        return self.x > other.x and self.y > other.y and self.z > other.z

    # Determine if Point is smaller than another Point
    def __lt__(self, other):
        return self.x < other.x and self.y < other.y and self.z < other.z

    # Create an iterator that iterates through each coordinate
    def __iter__(self):
        return (self.__getitem__(x) for x in range(3))

    # Override [] operator for syntactic sugar
    def __getitem__(self, item):
        if item == 0 or item == "X":
            return self.x
        if item == 1 or item == "Y":
            return self.y
        if item == 2 or item == "Z":
            return self.z


# Describes a motion
class Vector:
    def __init__(self, x, y, z):
        self.x = x  # Motion on x-axis
        self.y = y  # Motion on y-axis
        self.z = z  # Motion on z-axis

    # Add two motions together
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    # Divide a motion from another
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    # Scale a motion by a number
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)

    # Find the length of a vector
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    # Determine if two motions are the same
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # Syntactic sugar and for iteration
    def __getitem__(self, item):
        if item == 0 or item == "X":
            return self.x
        if item == 1 or item == "Y":
            return self.y
        if item == 2 or item == "Z":
            return self.y

    # Creates iterator that iterates through the coordinates
    def __iter__(self):
        return (self.__getitem__(x) for x in range(3))

    # Stringify vector, mainly used for debugging
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    # Make vector unit length in the same direction
    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    # Returns dot product of self and another
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # returns the cross product of self and another
    def cross(self, other):
        return Vector(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)
