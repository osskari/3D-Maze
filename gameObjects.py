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

    def set_position(self, new_position):
        self.position = new_position

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

    def create_walls(self, ambient, diffuse, specular):
        wall_size = 8
        grid_unit = 5
        # Borders
        # Vertical
        self.walls.append(Cube(ambient, diffuse, specular, Point(-50, wall_size / 2, -0), (100, wall_size, 0.1), 15))
        self.walls.append(Cube(ambient, diffuse, specular, Point(-50, wall_size / 2, -100), (100, wall_size, 0.1), 15))
        # Horizontal
        self.walls.append(Cube(ambient, diffuse, specular, Point(-100, wall_size / 2, -50), (0.1, wall_size, 100), 15))
        self.walls.append(Cube(ambient, diffuse, specular, Point(-0, wall_size / 2, -50), (0.1, wall_size, 100), 15))
        # Inside walls
        for wall in verticals:
            if wall[3] == "VERTICAL":
                self.walls.append(Cube(ambient, diffuse, specular, Point(-wall[1]*grid_unit, wall_size / 2, -wall[0]*grid_unit), (wall[2]*grid_unit, wall_size, 0.1), 15))
            elif wall[3] == "HORIZONTAL":
                self.walls.append(Cube(ambient, diffuse, specular, Point(-wall[0]*grid_unit, wall_size / 2, -wall[1]*grid_unit), (0.1, wall_size, wall[2]*grid_unit), 15))


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
            "D": False,   # Turn right
            "UP": False,  # Turn up
            "DOWN": False,   # Turn down
            "LEFT": False,   # Turn left
            "RIGHT": False   # Turn right
        }
# (grid_x, grid_y, length, direction)
verticals = [
    (1, 5.5, 5, "VERTICAL"),
    (1, 14, 10, "VERTICAL"),
    (2, 3.5, 1, "VERTICAL"),
    (2, 6.5, 1, "VERTICAL"),
    (2, 10.5, 5, "VERTICAL"),
    (2, 2.5, 1, "VERTICAL"),
    (2, 5.5, 1, "VERTICAL"),
    (3, 10, 4, "VERTICAL"),
    (4, 2.5, 1, "VERTICAL"),
    (4, 6, 2, "VERTICAL"),
    (4, 9, 2, "VERTICAL"),
    (4, 12.5, 1, "VERTICAL"),
    (5, 4.5, 1, "VERTICAL"),
    (5, 8, 4, "VERTICAL"),
    (6, 6, 6, "VERTICAL"),
    (6, 11.5, 2, "VERTICAL"),
    (6, 14.5, 1, "VERTICAL"),
    (6, 17.5, 1, "VERTICAL"),
    (7, 6.5, 7, "VERTICAL"),
    (7, 16.5, 5, "VERTICAL"),
    (8, 7, 8, "VERTICAL"),
    (8, 15, 2, "VERTICAL"),
    (9, 5, 2, "VERTICAL"),
    (9, 14, 2, "VERTICAL"),
    (10, 1, 2, "VERTICAL"),
    (10, 5.5, 1, "VERTICAL"),
    (10, 14.5, 1, "VERTICAL"),
    (11, 1.5, 1, "VERTICAL"),
    (11, 15.5, 1, "VERTICAL"),
    (11, 17.5, 1, "VERTICAL"),
    (12, 7, 4, "VERTICAL"),
    (12, 10.5, 1, "VERTICAL"),
    (12, 17.5, 3, "VERTICAL"),
    (13, 5, 4, "VERTICAL"),
    (13, 9.5, 3, "VERTICAL"),
    (13, 12.5, 1, "VERTICAL"),
    (13, 18, 4, "VERTICAL"),
    (14, 2, 2, "VERTICAL"),
    (14, 5.5, 3, "VERTICAL"),
    (14, 9, 2, "VERTICAL"),
    (14, 11.5, 1, "VERTICAL"),
    (14, 13.5, 1, "VERTICAL"),
    (14, 16, 2, "VERTICAL"),
    (14, 18.5, 1, "VERTICAL"),
    (15, 1.5, 3, "VERTICAL"),
    (15, 5, 2, "VERTICAL"),
    (15, 10, 2, "VERTICAL"),
    (15, 14.5, 5, "VERTICAL"),
    (16, 3.5, 5, "VERTICAL"),
    (16, 14.5, 3, "VERTICAL"),
    (17, 13.5, 1, "VERTICAL"),
    (18, 11, 6, "VERTICAL"),
    (18, 16, 2, "VERTICAL"),
    (19, 2, 2, "VERTICAL"),
    (19, 5, 2, "VERTICAL"),
    (19, 10, 6, "VERTICAL"),
    (19, 16, 4, "VERTICAL"),

    (1, 6, 6, "HORIZONTAL"),
    (1, 12.5, 3, "HORIZONTAL"),
    (1, 17, 2, "HORIZONTAL"),
    (2, 3.5, 1, "HORIZONTAL"),
    (2, 7.5, 5, "HORIZONTAL"),
    (2, 12, 2, "HORIZONTAL"),
    (2, 18, 2, "HORIZONTAL"),
    (3, 2.5, 1, "HORIZONTAL"),
    (3, 5, 2, "HORIZONTAL"),
    (3, 12, 8, "HORIZONTAL"),
    (3, 18, 2, "HORIZONTAL"),
    (4, 4, 2, "HORIZONTAL"),
    (4, 11, 4, "HORIZONTAL"),
    (4, 14.5, 1, "HORIZONTAL"),
    (4, 18, 2, "HORIZONTAL"),
    (5, 2, 2, "HORIZONTAL"),
    (5, 4.5, 1, "HORIZONTAL"),
    (5, 11, 2, "HORIZONTAL"),
    (5, 17, 2, "HORIZONTAL"),
    (6, 10.5, 1, "HORIZONTAL"),
    (6, 17.5, 3, "HORIZONTAL"),
    (7, 3, 2, "HORIZONTAL"),
    (7, 10, 4, "HORIZONTAL"),
    (7, 16.5, 5, "HORIZONTAL"),
    (8, 3, 4, "HORIZONTAL"),
    (8, 16, 4, "HORIZONTAL"),
    (9, 0.5, 1, "HORIZONTAL"),
    (9, 16, 2, "HORIZONTAL"),
    (10, 6.5, 1, "HORIZONTAL"),
    (10, 17, 2, "HORIZONTAL"),
    (11, 4, 2, "HORIZONTAL"),
    (11, 12, 12, "HORIZONTAL"),
    (11, 19.5, 1, "HORIZONTAL"),
    (12, 9.5, 7, "HORIZONTAL"),
    (12, 15.5, 3, "HORIZONTAL"),
    (13, 7.5, 11, "HORIZONTAL"),
    (13, 16.5, 1, "HORIZONTAL"),
    (14, 3, 4, "HORIZONTAL"),
    (14, 8.5, 1, "HORIZONTAL"),
    (14, 12, 4, "HORIZONTAL"),
    (14, 18.5, 1, "HORIZONTAL"),
    (15, 4, 4, "HORIZONTAL"),
    (15, 9.5, 1, "HORIZONTAL"),
    (15, 12.5, 3, "HORIZONTAL"),
    (15, 17, 2, "HORIZONTAL"),
    (16, 3.5, 3, "HORIZONTAL"),
    (16, 9.5, 3, "HORIZONTAL"),
    (16, 12.5, 1, "HORIZONTAL"),
    (16, 16.5, 1, "HORIZONTAL"),
    (17, 2, 2, "HORIZONTAL"),
    (17, 5, 2, "HORIZONTAL"),
    (17, 9, 4, "HORIZONTAL"),
    (17, 16.5, 3, "HORIZONTAL"),
    (18, 4, 4, "HORIZONTAL"),
    (18, 9.5, 3, "HORIZONTAL"),
    (18, 16.5, 3, "HORIZONTAL"),
    (19, 4.5, 5, "HORIZONTAL"),
    (19, 10, 4, "HORIZONTAL"),
    (19, 16.5, 5, "HORIZONTAL"),
]
