from baseObjects import *


class ModelMatrix:
    def __init__(self):
        self.matrix = [1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]
        self.stack = []
        self.stack_count = 0
        self.stack_capacity = 0

    def load_identity(self):
        self.matrix = [1, 0, 0, 0,
                       0, 1, 0, 0,
                       0, 0, 1, 0,
                       0, 0, 0, 1]

    def copy_matrix(self):
        new_matrix = [0] * 16
        for i in range(16):
            new_matrix[i] = self.matrix[i]
        return new_matrix

    def add_transformation(self, matrix2):
        counter = 0
        new_matrix = [0] * 16
        for row in range(4):
            for col in range(4):
                for i in range(4):
                    new_matrix[counter] += self.matrix[row * 4 + i] * matrix2[col + 4 * i]
                counter += 1
        self.matrix = new_matrix

    def add_nothing(self):
        other_matrix = [1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_translation(self, x, y, z):
        other_matrix = [1, 0, 0, x,
                        0, 1, 0, y,
                        0, 0, 1, z,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_scale(self, sx, sy, sz):
        other_matrix = [sx, 0, 0, 0,
                        0, sy, 0, 0,
                        0, 0, sz, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_x_rotation(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [1, 0, 0, 0,
                        0, c, -s, 0,
                        0, s, c, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_y_rotation(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [c, 0, s, 0,
                        0, 1, 0, 0,
                        -s, 0, c, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def add_z_rotation(self, angle):
        c = cos(angle)
        s = sin(angle)
        other_matrix = [c, -s, 0, 0,
                        s, c, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1]
        self.add_transformation(other_matrix)

    def push_matrix(self):
        self.stack.append(self.copy_matrix())

    def pop_matrix(self):
        self.matrix = self.stack.pop()

    def __str__(self):
        ret_str = ""
        counter = 0
        for _ in range(4):
            ret_str += "["
            for _ in range(4):
                ret_str += " " + str(self.matrix[counter]) + " "
                counter += 1
            ret_str += "]\n"
        return ret_str


class ViewMatrix:
    def __init__(self):
        self.eye = Point(0, 0, 0)
        self.u = Vector(1, 0, 0)
        self.v = Vector(0, 1, 0)
        self.n = Vector(0, 0, 1)

    def look(self, eye, center, up):
        self.eye = eye
        self.n = (eye - center)
        self.n.normalize()
        self.u = up.cross(self.n)
        self.u.normalize()
        self.v = self.n.cross(self.u)

    def slide(self, del_u, del_v, del_n):
        return self.u * del_u + self.v * del_v + self.n * del_n

    def roll(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.v * s
        self.v = self.u * -s + self.v * c
        self.u = tmp_u

    def pitch(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_v = self.v * c + self.n * -s
        self.n = self.v * s + self.n * c
        self.v = tmp_v

    def yaw(self, angle):
        c = cos(angle)
        s = sin(angle)

        tmp_u = self.u * c + self.n * s
        self.n = self.u * -s + self.n * c
        self.u = tmp_u

    def rotate_y(self, angle):
        c = cos(angle)
        s = -sin(angle)

        self.u = Vector(c * self.u.x - s * self.u.z, self.u.y, s * self.u.x + c * self.u.z)
        self.v = Vector(c * self.v.x - s * self.v.z, self.v.y, s * self.v.x + c * self.v.z)
        self.n = Vector(c * self.n.x - s * self.n.z, self.n.y, s * self.n.x + c * self.n.z)

    def walk(self, delta):
        return Vector(delta * self.n.x, 0, delta * self.n.z)

    def is_between(self, new_pos, drawable):
        scale_x, scale_y, scale_z = drawable.scale
        return Point(drawable.position.x - scale_x / 2 - drawable.offset,
                     drawable.position.y - scale_y / 2 - drawable.offset,
                     drawable.position.z - scale_z / 2 - drawable.offset) \
               < self.eye + new_pos \
               < Point(drawable.position.x + scale_x / 2 + drawable.offset,
                       drawable.position.y + scale_y / 2 + drawable.offset,
                       drawable.position.z + scale_z / 2 + drawable.offset)

    def get_matrix(self):
        minus_eye = Vector(-self.eye.x, -self.eye.y, -self.eye.z)
        return [self.u.x, self.u.y, self.u.z, minus_eye.dot(self.u),
                self.v.x, self.v.y, self.v.z, minus_eye.dot(self.v),
                self.n.x, self.n.y, self.n.z, minus_eye.dot(self.n),
                0, 0, 0, 1]


class ProjectionMatrix:
    def __init__(self):
        self.left = -1
        self.right = 1
        self.bottom = -1
        self.top = 1
        self.near = -1
        self.far = 1

        self.is_orthographic = True

    def set_perspective(self, fov_y, aspect, near, far):
        self.near = near
        self.far = far
        self.top = near * tan(fov_y / 2)
        self.bottom = -self.top
        self.right = self.top * aspect
        self.left = -self.right
        self.is_orthographic = False

    def set_orthographic(self, left, right, bottom, top, near, far):
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top
        self.near = near
        self.far = far
        self.is_orthographic = True

    def get_matrix(self):
        if self.is_orthographic:
            a = 2 / (self.right - self.left)
            b = -(self.right + self.left) / (self.right - self.left)
            c = 2 / (self.top - self.bottom)
            d = -(self.top + self.bottom) / (self.top - self.bottom)
            e = 2 / (self.near - self.far)
            f = (self.near + self.far) / (self.near - self.far)

            return [a, 0, 0, b,
                    0, c, 0, d,
                    0, 0, e, f,
                    0, 0, 0, 1]

        else:
            a = (2 * self.near) / (self.right - self.left)
            b = (self.right + self.left) / (self.right - self.left)
            c = (2 * self.near) / (self.top - self.bottom)
            d = (self.top + self.bottom) / (self.top - self.bottom)
            e = -(self.far + self.near) / (self.far - self.near)
            f = -(2 * self.far * self.near) / (self.far - self.near)
            return [a, 0, b, 0,
                    0, c, d, 0,
                    0, 0, e, f,
                    0, 0, -1, 0]
