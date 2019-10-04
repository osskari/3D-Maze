# from math import *
# # from baseObjects import Point, Vector
#
#
# class Game:
#     def __init__(self, shader, model_matrix, view_matrix, projection_matrix, player):
#         self.shader = shader
#         shader.use()
#         self.model_matrix = model_matrix
#         self.view_matrix = view_matrix
#         self.player = player
#         self.look()
#         self.projection_matrix = projection_matrix
#
#     def look(self):
#         self.view_matrix.look(self.player.position, self.player.looking_at, self.player.normal)
#
#     def set_perspective(self, fov, aspect, near, far):
#         self.projection_matrix.set_perspective(fov, aspect, near, far)
#         self.shader.set_projection_matrix(self.projection_matrix.get_matrix())
#
#
# class Player:
#     def __init__(self, position, speed, rotation_speed, looking_at):
#         self.position = position
#         self.speed = speed
#         self.rotationSpeed = rotation_speed
#         self.looking_at = Point(looking_at.x, self.position.y, looking_at.z)
#         self.normal = Vector(0, 1, 0)
#
#
# class Drawable:
#     def __init__(self, diffuse, specular, position, scale, shininess):
#         self.diffuse = diffuse
#         self.specular = specular
#         self.position = position
#         self.scale = scale
#         self.shininess = shininess
#
#
# class Rectangle(Drawable):
#     def __init__(self, color, position, scale):
#         Drawable.__init__(self, color, position, scale)
#
#     def draw(self, model_matrix, shader, cube):
#         # shader.set_solid_color(*self.color)
#         model_matrix.add_translation(*self.position)
#         # model_matrix.push_matrix()
#         model_matrix.add_scale(*self.scale)
#         shader.set_model_matrix(model_matrix.matrix)
#         cube.draw()
#         # model_matrix.pop_matrix()
#
#
# class Maze:
#     def __init__(self):
#         self.walls = []
#         self.lights = []
#
#
# class Level:
#     def __init__(self, floor, maze):
#         self.floor = floor
#         self.maze = maze
#
#     def collision(self, new_pos, offset, matrix):
#         for wall in self.maze.walls:
#             if matrix.is_between(new_pos, wall, offset):
#                 return wall
#         return None
#
#
# class Light:
#     def __init__(self, position, diffuse, spectral=None):
#         self.position = position
#         self.diffuse = diffuse
#         self.spectral = spectral if spectral else diffuse
#
#
# inputs = {
#             "W": False,  # Walk forward
#             "A": False,  # Turn left
#             "S": False,  # Walk backwards
#             "D": False   # Turn right
#         }
