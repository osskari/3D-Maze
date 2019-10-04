from matrices import *
from shaders import *


class Cube(Drawable):
    def __init__(self, ambient, diffuse, specular, position, scale, shininess):
        Drawable.__init__(self, ambient, diffuse, specular, position, scale, shininess, 0.5)
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

    def draw(self, model_matrix, shader):
        super(Cube, self).draw(model_matrix, shader)
        # draw
        for i in range(0, 21, 4):
            glDrawArrays(GL_TRIANGLE_FAN, i, 4)


class Sphere(Drawable):
    def __init__(self, ambient, diffuse, specular, position, scale, shininess, stacks=12, slices=24):
        Drawable.__init__(self, ambient, diffuse, specular, position, scale, shininess, 3)
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
        self.position_array = self.vertex_array
        self.normal_array = self.vertex_array

    def draw(self, model_matrix, shader):
        super(Sphere, self).draw(model_matrix, shader)
        # draw
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)


class Game:
    def __init__(self, player):
        self.shader = Shader3D()
        self.shader.use()
        self.shader.set_global_ambient(1, 1, 1)
        self.model_matrix = ModelMatrix()
        self.view_matrix = ViewMatrix()
        self.player = player
        self.look()
        self.projection_matrix = ProjectionMatrix()
        self.maze = Maze()

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


class Maze:
    def __init__(self):
        self.floor = Cube((0.15, 0.1, 0.1), (0.9, 0.6, 0.5), (0.7, 0.4, 0.4), Point(0, -0.1, 0), (100, 0.1, 100), 15)
        self.walls = []
        self.lights = []

    def collision(self, new_pos, matrix):
        for wall in self.walls:
            if matrix.is_between(new_pos, wall):
                return wall
        return None


class Light:
    def __init__(self, position, ambient, diffuse=None, specular=None):
        self.position = position
        self.ambient = ambient
        # If only ambient is provided then diff and spec are the same
        self.diffuse = diffuse if diffuse else ambient
        self.specular = specular if specular else diffuse


inputs = {
            "W": False,  # Walk forward
            "A": False,  # Turn left
            "S": False,  # Walk backwards
            "D": False   # Turn right
        }
