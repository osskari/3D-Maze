import pygame
from pygame.locals import *

from gameObjects import *


class Maze3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.game = Game(Player(Point(-5, 3, -5), 10, pi, Point(-6, 3, -6)))

        self.game.look()
        self.game.set_perspective(pi / 2, 800 / 600, 0.3, 300)

        self.inputs = inputs
        self.game.maze.create_walls((0.1, 0.01, 0.01), (0.6, 0.6, 0.6), (0.9, 0.5, 0.2))
        self.game.maze.create_lights(self.game.player.position)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.sun_angle = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        # Update position of the sun
        self.sun_angle += (pi / 2) * delta_time
        if self.sun_angle > 20 * pi:
            self.sun_angle = 0

        # Handle user input
        if self.inputs["W"]:
            if self.game.maze.update_player(self.game.view_matrix, self.game.player.speed, delta_time):
                return True
        if self.inputs["S"]:
            if self.game.maze.update_player(self.game.view_matrix, -self.game.player.speed, delta_time):
                return True
        if self.inputs["A"]:
            # self.game.view_matrix.yaw(-self.game.player.rotationSpeed * delta_time)
            self.game.view_matrix.rotate_y(self.game.player.rotationSpeed * delta_time)
        if self.inputs["D"]:
            # self.game.view_matrix.yaw(self.game.player.rotationSpeed * delta_time)
            self.game.view_matrix.rotate_y(-self.game.player.rotationSpeed * delta_time)
        if self.inputs["LEFT"]:
            # self.game.view_matrix.yaw(-self.game.player.rotationSpeed * delta_time)
            self.game.view_matrix.rotate_y(self.game.player.rotationSpeed * delta_time)
        if self.inputs["RIGHT"]:
            # self.game.view_matrix.yaw(self.game.player.rotationSpeed * delta_time)
            self.game.view_matrix.rotate_y(-self.game.player.rotationSpeed * delta_time)
        if self.inputs["DOWN"]:
            self.game.view_matrix.pitch(self.game.player.rotationSpeed * delta_time)
        if self.inputs["UP"]:
            self.game.view_matrix.pitch(-self.game.player.rotationSpeed * delta_time)

        self.game.player.position = self.game.view_matrix.eye
        self.game.maze.sun.set_position(Point(0, -sin(self.sun_angle / 10) * 100, cos(self.sun_angle / 10) * 100))
        self.game.maze.lights[0].position = self.game.view_matrix.eye
        self.game.maze.lights[1].position = self.game.maze.sun.position
        return False

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, 800, 600)

        self.game.shader.set_view_matrix(self.game.view_matrix.get_matrix())

        self.game.shader.set_light_position(self.game.maze.get_light_positions())
        self.game.shader.set_light_color(self.game.maze.get_light_ambient())

        self.game.model_matrix.load_identity()

        # Draw stuff
        self.game.maze.draw_maze(self.game.shader, self.game.model_matrix)

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting!")
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("Escaping!")
                    return True
                if event.key == K_w:
                    self.inputs["W"] = True
                if event.key == K_s:
                    self.inputs["S"] = True
                if event.key == K_a:
                    self.inputs["A"] = True
                if event.key == K_d:
                    self.inputs["D"] = True
                if event.key == K_UP:
                    self.inputs["UP"] = True
                if event.key == K_DOWN:
                    self.inputs["DOWN"] = True
                if event.key == K_RIGHT:
                    self.inputs["RIGHT"] = True
                if event.key == K_LEFT:
                    self.inputs["LEFT"] = True
            elif event.type == pygame.KEYUP:
                if event.key == K_w:
                    self.inputs["W"] = False
                if event.key == K_s:
                    self.inputs["S"] = False
                if event.key == K_a:
                    self.inputs["A"] = False
                if event.key == K_d:
                    self.inputs["D"] = False
                if event.key == K_UP:
                    self.inputs["UP"] = False
                if event.key == K_DOWN:
                    self.inputs["DOWN"] = False
                if event.key == K_RIGHT:
                    self.inputs["RIGHT"] = False
                if event.key == K_LEFT:
                    self.inputs["LEFT"] = False
        return False

    def program_loop(self):
        exiting = False
        while not exiting:
            exiting = self.events()
            if not exiting:
                exiting = self.update()
            if not exiting:
                self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    Maze3D().start()
