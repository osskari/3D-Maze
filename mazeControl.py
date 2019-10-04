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

        self.game = Game(Player(Point(0, 3, 10), 10, pi, Point(0, 1, 0)))

        self.game.look()
        self.game.set_perspective(pi/2, 800/600, 0.3, 100)

        self.cube = Cube((0.1, 0.01, 0.01),
                         (0.6, 0.6, 0.6),
                         (0.9, 0.5, 0.2),
                         Point(9.0, 3.0, -2.0),
                         (4, 5, 15),
                         13
                         )
        self.sphere = Sphere((0.3, 0.3, 0.3),
                             (0.7, 0.5, 0.4),
                             (0.9, 0.8, 0.5),
                             Point(0, 3, 2),
                             (5, 5, 5),
                             17
                             )
        self.inputs = inputs
        self.game.maze.walls.append(self.cube)
        self.game.maze.walls.append(self.sphere)
        self.game.maze.lights.append(Light(self.game.player.position, (1.0, 1.0, 1.0)))

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        if self.angle > 2 * pi:
            self.angle -= (2 * pi)

        if self.inputs["W"]:
            newpos = self.game.view_matrix.slide(0, 0, -self.game.player.speed * delta_time)
            if not self.game.maze.collision(newpos, self.game.view_matrix):
                self.game.view_matrix.eye += newpos
        if self.inputs["S"]:
            newpos = self.game.view_matrix.slide(0, 0, self.game.player.speed * delta_time)
            if not self.game.maze.collision(newpos, self.game.view_matrix):
                self.game.view_matrix.eye += newpos
        if self.inputs["A"]:
            self.game.view_matrix.yaw(-self.game.player.rotationSpeed * delta_time)
        if self.inputs["D"]:
            self.game.view_matrix.yaw(self.game.player.rotationSpeed * delta_time)
        self.game.player.position = self.game.view_matrix.eye
        self.game.maze.lights[0].position = self.game.view_matrix.eye

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.game.shader.set_view_matrix(self.game.view_matrix.get_matrix())

        self.game.shader.set_light_position(*self.game.maze.lights[0].position)
        self.game.shader.set_light_color(*self.game.maze.lights[0].ambient)

        self.game.model_matrix.load_identity()

        # Draw stuff

        # Draw walls
        for wall in self.game.maze.walls:
            wall.set_vertices(self.game.shader)
            wall.set_color(self.game.shader)
            self.game.model_matrix.push_matrix()
            wall.draw(self.game.model_matrix, self.game.shader)
            self.game.model_matrix.pop_matrix()

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
