import pygame
from pygame.locals import *

from gameObjects import *


class Maze3D:
    def __init__(self):
        pygame.init()
        pygame.display.set_mode((800, 600), pygame.OPENGL | pygame.DOUBLEBUF)

        self.game = Game(Player(Point(0, 3, 10), 10, pi, Point(0, 1, 0)))

        self.game.look()
        self.game.set_perspective(pi/2, 800/600, 0.3, 300)

        self.sun = Sphere((1.0, 0.4, 0.3),
                          (0.8, 0.7, 0.1),
                          (0.9, 0.2, 0.2),
                          Point(0, pi, pi),
                          (5, 5, 5),
                          100)

        self.inputs = inputs
        self.game.maze.create_walls((0.1, 0.01, 0.01), (0.6, 0.6, 0.6), (0.9, 0.5, 0.2))

        self.game.maze.lights.append(Light(self.game.player.position, (1.0, 1.0, 1.0)))

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0
        self.sun_angle = 0

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.sun_angle += (pi/2) * delta_time
        if self.sun_angle > 20 * pi:
            self.sun_angle = 0

        self.angle += pi * delta_time
        if self.angle > 2 * pi:
            self.angle -= (2 * pi)

        if self.inputs["W"]:
            new_pos = self.game.view_matrix.slide(0, 0, -self.game.player.speed * delta_time)
            collision_wall = self.game.maze.collision(new_pos, self.game.view_matrix)
            if not collision_wall:
                self.game.view_matrix.eye += new_pos
            else:
                self.game.view_matrix.eye += self.game.maze.slide(self.game.view_matrix.eye, new_pos, collision_wall)
        if self.inputs["S"]:
            new_pos = self.game.view_matrix.slide(0, 0, self.game.player.speed * delta_time)
            collision_wall = self.game.maze.collision(new_pos, self.game.view_matrix)
            if not collision_wall:
                self.game.view_matrix.eye += new_pos
            else:
                self.game.view_matrix.eye += self.game.maze.slide(self.game.view_matrix.eye, new_pos, collision_wall)
        if self.inputs["A"]:
            self.game.view_matrix.yaw(-self.game.player.rotationSpeed * delta_time)
        if self.inputs["D"]:
            self.game.view_matrix.yaw(self.game.player.rotationSpeed * delta_time)
        if self.inputs["LEFT"]:
            self.game.view_matrix.yaw(-self.game.player.rotationSpeed * delta_time)
        if self.inputs["RIGHT"]:
            self.game.view_matrix.yaw(self.game.player.rotationSpeed * delta_time)
        if self.inputs["DOWN"]:
            self.game.view_matrix.pitch(self.game.player.rotationSpeed * delta_time)
        if self.inputs["UP"]:
            self.game.view_matrix.pitch(-self.game.player.rotationSpeed * delta_time)

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

        # Draw sphere
        self.sun.set_vertices(self.game.shader)
        self.sun.set_color(self.game.shader)
        self.game.model_matrix.push_matrix()
        self.sun.set_position(Point(0, -sin(self.sun_angle/10) * 100, cos(self.sun_angle/10) * 100))
        self.sun.draw(self.game.model_matrix, self.game.shader)
        self.game.model_matrix.pop_matrix()

        self.game.shader.set_light_position(*self.sun.position)
        self.game.shader.set_light_color(0.5, 0.5, 0.5)

        self.game.maze.walls[0].set_vertices(self.game.shader)
        for wall in self.game.maze.walls:
            wall.set_color(self.game.shader)
            self.game.model_matrix.push_matrix()
            wall.draw(self.game.model_matrix, self.game.shader)
            self.game.model_matrix.pop_matrix()


        # Draw floor
        self.game.maze.floor.set_vertices(self.game.shader)
        self.game.maze.floor.set_color(self.game.shader)
        self.game.model_matrix.push_matrix()
        self.game.maze.floor.draw(self.game.model_matrix, self.game.shader)
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
