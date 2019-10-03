from math import *

import pygame
from pygame.locals import *

import sys
import time

from shaders import *
from matrices import *
from gameObjects import *


class Maze3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()

        self.player = Player(Point(0, 3, 10), 5, pi, Point(0, 1, 0))

        self.view_matrix.look(self.player.position, self.player.looking_at, self.player.normal)

        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(pi/2, 800/600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.level = Level(Drawable((0.0, 1.0, 0.0), Point(5.0, 0.0, 5.0), (100.0, 0.1, 100.0)))
        self.inputs = inputs

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        if self.angle > 2 * pi:
            self.angle -= (2 * pi)

        if self.inputs["W"]:
            self.view_matrix.slide(0, 0, -self.player.speed * delta_time)
        if self.inputs["S"]:
            self.view_matrix.slide(0, 0, self.player.speed * delta_time)
        if self.inputs["A"]:
            self.view_matrix.yaw(-self.player.rotationSpeed * delta_time)
        if self.inputs["D"]:
            self.view_matrix.yaw(self.player.rotationSpeed * delta_time)
        self.player.position = self.view_matrix.eye

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.model_matrix.load_identity()

        # Draw stuff
        if Point(9.0 - 1.5, 3.0 - 1.5, -2.0 - 1.5) < self.player.position < Point(9.0+1.5, 3.0+1.5, -2.0+1.5):
            print(self.player.position)

        self.cube.set_vertices(self.shader)

        self.shader.set_solid_color(1.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(9.0, 3.0, -2.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        # Draw floor
        self.shader.set_solid_color(*self.level.floor.color)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(*self.level.floor.position.to_list())
        self.model_matrix.add_scale(*self.level.floor.size)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        pygame.display.flip()

    def events(self, exiting):
        ret_val = exiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting!")
                ret_val = True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("Escaping!")
                    ret_val = True
                if event.key == K_w:
                    self.inputs["W"] = True
                if event.key == K_s:
                    self.inputs["S"] = True
                if event.key == K_a:
                    self.inputs["A"] = True
                if event.key == K_d:
                    self.inputs["D"] = True
            elif event.type == pygame.KEYUP:
                if event.key == K_w:
                    self.inputs["W"] = False
                if event.key == K_s:
                    self.inputs["S"] = False
                if event.key == K_a:
                    self.inputs["A"] = False
                if event.key == K_d:
                    self.inputs["D"] = False
        return ret_val

    def program_loop(self):
        exiting = False
        while not exiting:
            exiting = self.events(exiting)
            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    Maze3D().start()
