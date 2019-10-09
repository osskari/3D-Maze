import sys

from baseObjects import *


class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader, shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader, shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if result != 1:  # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        # Link shaders
        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        # Matrices
        self.modelMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        # Camera
        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")

        # Global ambient
        self.globalAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_global_ambient")

        # Light
        # Position of light sources
        self.lightPosLoc = [glGetUniformLocation(self.renderingProgramID, "u_light_position_1"),
                            glGetUniformLocation(self.renderingProgramID, "u_light_position_2"),
                            glGetUniformLocation(self.renderingProgramID, "u_light_position_3")]
        # Ambient of light sources
        self.lightAmbientLoc = [glGetUniformLocation(self.renderingProgramID, "u_light_ambient_1"),
                                glGetUniformLocation(self.renderingProgramID, "u_light_ambient_2"),
                                glGetUniformLocation(self.renderingProgramID, "u_light_ambient_3")]
        # Diffuse of light sources
        self.lightDiffuseLoc = [glGetUniformLocation(self.renderingProgramID, "u_light_diffuse1"),
                                glGetUniformLocation(self.renderingProgramID, "u_light_diffuse2"),
                                glGetUniformLocation(self.renderingProgramID, "u_light_diffuse3")]
        # Specular of light sources
        self.lightSpecularLoc = [glGetUniformLocation(self.renderingProgramID, "u_light_specular_1"),
                                 glGetUniformLocation(self.renderingProgramID, "u_light_specular_2"),
                                 glGetUniformLocation(self.renderingProgramID, "u_light_specular_3")]

        # Material
        # Material position
        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)
        # Material orientation
        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)
        # Ambient of material
        self.materialAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_ambient")
        # Diffuse of material
        self.materialDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_diffuse")
        # Specular of material
        self.materialSpecularLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_specular")
        # Shininess of material
        self.materialShininessLoc = glGetUniformLocation(self.renderingProgramID, "u_mat_shininess")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    # Matrices
    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    # Eye
    def set_eye_position(self, x, y, z):
        glUniform4f(self.eyePosLoc, x, y, z, 1.0)

    # Global
    def set_global_ambient(self, x, y, z):
        glUniform4f(self.globalAmbientLoc, x, y, z, 1.0)

    # Light
    def set_light_position(self, lights):
        for i, light in enumerate(lights):
            glUniform4f(self.lightPosLoc[i], light.x, light.y, light.z, 1.0)

    def set_light_color(self, lights):
        self.set_light_ambient(lights)
        self.set_light_diffuse(lights)
        self.set_light_specular(lights)

    def set_light_ambient(self, lights):
        for i, light in enumerate(lights):
            glUniform4f(self.lightAmbientLoc[i], light["r"], light["g"], light["b"], 1.0)

    def set_light_diffuse(self, lights):
        for i, light in enumerate(lights):
            glUniform4f(self.lightDiffuseLoc[i], light["r"], light["g"], light["b"], 1.0)

    def set_light_specular(self, lights):
        for i, light in enumerate(lights):
            glUniform4f(self.lightSpecularLoc[i], light["r"], light["g"], light["b"], 1.0)

    # Material
    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, normal_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, True, 0, normal_array)

    def set_material_ambient(self, r, g, b):
        glUniform4f(self.materialAmbientLoc, r, g, b, 1.0)

    def set_material_diffuse(self, r, g, b):
        glUniform4f(self.materialDiffuseLoc, r, g, b, 1.0)

    def set_material_specular(self, r, g, b):
        glUniform4f(self.materialSpecularLoc, r, g, b, 1.0)

    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)
