from baseObjects import Point, Vector


class Player:
    def __init__(self, position, speed, rotation_speed, looking_at):
        self.position = position
        self.speed = speed
        self.rotationSpeed = rotation_speed
        self.looking_at = Point(looking_at.x, self.position.y, looking_at.z)
        self.normal = Vector(0, 1, 0)


class Level:
    def __init__(self, floor):
        self.floor = floor


class Drawable:
    def __init__(self, color, position, size):
        self.color = color
        self.position = position
        self.size = size


inputs = {
            "W": False,  # Walk forward
            "A": False,  # Turn left
            "S": False,  # Walk backwards
            "D": False   # Turn right
        }
