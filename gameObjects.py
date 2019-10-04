from baseObjects import Point, Vector


class Player:
    def __init__(self, position, speed, rotation_speed, looking_at):
        self.position = position
        self.speed = speed
        self.rotationSpeed = rotation_speed
        self.looking_at = Point(looking_at.x, self.position.y, looking_at.z)
        self.normal = Vector(0, 1, 0)


class Drawable:
    def __init__(self, color, position, scale):
        self.color = color
        self.position = position
        self.scale = scale


class Rectangle(Drawable):
    def __init__(self, color, position, scale):
        Drawable.__init__(self, color, position, scale)

    def draw(self, model_matrix, shader, cube):
        shader.set_solid_color(*self.color)
        model_matrix.add_translation(*self.position)
        # model_matrix.push_matrix()
        model_matrix.add_scale(*self.scale)
        shader.set_model_matrix(model_matrix.matrix)
        cube.draw()
        # model_matrix.pop_matrix()


class Maze:
    def __init__(self):
        self.walls = []


class Level:
    def __init__(self, floor, maze):
        self.floor = floor
        self.maze = maze

    def collision(self, new_pos, offset, matrix):
        for wall in self.maze.walls:
            if matrix.is_between(new_pos, wall, offset):
                return wall
        return None


inputs = {
            "W": False,  # Walk forward
            "A": False,  # Turn left
            "S": False,  # Walk backwards
            "D": False   # Turn right
        }
