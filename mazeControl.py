from math import *

import pygame
from pygame.locals import *

import sys
import time

from shaders import *
from matrices import *


class Maze3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 3, 10), Point(0, 0, 0), Vector(0, 1, 0))

        self.projection_matrix = ProjectionMatrix()
        # self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(pi/2, 800/600, 0.5, 100)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False
        self.w_key_down = False
        self.s_key_down = False
        self.a_key_down = False
        self.d_key_down = False
        self.q_key_down = False
        self.e_key_down = False

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.angle += pi * delta_time
        # if angle > 2 * pi:
        #     angle -= (2 * pi)

        if self.w_key_down:
            self.view_matrix.slide(0, 0, -1 * delta_time)
        if self.s_key_down:
            self.view_matrix.slide(0, 0, 1 * delta_time)
        if self.a_key_down:
            self.view_matrix.slide(-1 * delta_time, 0, 0)
        if self.d_key_down:
            self.view_matrix.slide(1 * delta_time, 0, 0)
        if self.q_key_down:
            self.view_matrix.roll(-pi * delta_time)
        if self.e_key_down:
            self.view_matrix.roll(pi * delta_time)
        if self.UP_key_down:
            self.white_background = True
        else:
            self.white_background = False

    def display(self):
        glEnable(GL_DEPTH_TEST)

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.model_matrix.load_identity()

        # Draw stuff

        self.cube.set_vertices(self.shader)

        self.shader.set_solid_color(1.0, 0.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(9.0, 5.0, -2.0)
        self.model_matrix.add_scale(2.0, 2.0, 2.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.shader.set_solid_color(0.0, 1.0, 0.0)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(-5.0, -0.8, -5.0)
        self.model_matrix.add_scale(10.0, 0.8, 10.0)
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
                if event.key == K_UP:
                    self.UP_key_down = True
                if event.key == K_w:
                    self.w_key_down = True
                if event.key == K_s:
                    self.s_key_down = True
                if event.key == K_a:
                    self.a_key_down = True
                if event.key == K_d:
                    self.d_key_down = True
                if event.key == K_q:
                    self.q_key_down = True
                if event.key == K_e:
                    self.e_key_down = True
            elif event.type == pygame.KEYUP:
                if event.key == K_UP:
                    self.UP_key_down = False
                if event.key == K_w:
                    self.w_key_down = False
                if event.key == K_s:
                    self.s_key_down = False
                if event.key == K_a:
                    self.a_key_down = False
                if event.key == K_d:
                    self.d_key_down = False
                if event.key == K_q:
                    self.q_key_down = False
                if event.key == K_e:
                    self.e_key_down = False
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
