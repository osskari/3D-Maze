uniform vec4 u_global_ambient; // Global ambient colour

uniform vec4 u_light_ambient_1; // Ambient for light 1
uniform vec4 u_light_ambient_2; // Ambient for light 2
uniform vec4 u_light_ambient_3; // Ambient for light 3
uniform vec4 u_mat_ambient; // Ambient for material

uniform vec4 u_light_diffuse_1; // Diffuse for light 1
uniform vec4 u_light_diffuse_2; // Diffuse for light 2
uniform vec4 u_light_diffuse_3; // Diffuse for light 3
uniform vec4 u_mat_diffuse; // Diffuse for material

uniform vec4 u_light_specular_1; // Specular for light 1
uniform vec4 u_light_specular_2; // Specular for light 2
uniform vec4 u_light_specular_3; // Specular for light 3
uniform vec4 u_mat_specular; // Specular for material

uniform float u_mat_shininess; // Material shininess

varying vec4 v_normal; // Material normal

varying vec4 v_s_1; // S vector for light 1
varying vec4 v_h_1; // H vector for light 1

varying vec4 v_s_2; // S vector for light 2
varying vec4 v_h_2; // H vector for light 2

varying vec4 v_s_3; // S vector for light 3
varying vec4 v_h_3; // H vector for light 3

void main(void)
{
    // Lambert value for light 1
	float lambert_1 = max(dot(v_normal, v_s_1), 0);
    // Phong value for light 1
	float phong_1 = max(dot(v_normal, v_h_1), 0);

    // Lambert value for light 2
    float lambert_2 = max(dot(v_normal, v_s_2), 0);
    // Phong value for light 2
	float phong_2 = max(dot(v_normal, v_h_2), 0);

    // Lambert value for light 2
    float lambert_3 = max(dot(v_normal, v_s_3), 0);
    // Phong value for light 2
	float phong_3 = max(dot(v_normal, v_h_3), 0);

    // I = light_amb * mat_amb + light_diff * mat_amb * lambert + light_spec * mat_spec * phong
    // I for light 1
    vec4 i_1 = u_light_ambient_1 * u_mat_ambient
                   + lambert_1 * u_light_diffuse_1 * u_mat_diffuse
                   + u_light_specular_1 * u_mat_specular * pow(phong_1, u_mat_shininess);
    // I for light 2
    vec4 i_2 = u_light_ambient_2 * u_mat_ambient
                   + lambert_2 * u_light_diffuse_2 * u_mat_diffuse
                   + u_light_specular_2 * u_mat_specular * pow(phong_2, u_mat_shininess);
     // I for light 2
    vec4 i_3 = u_light_ambient_3 * u_mat_ambient
                   + lambert_3 * u_light_diffuse_3 * u_mat_diffuse
                   + u_light_specular_3 * u_mat_specular * pow(phong_3, u_mat_shininess);

    // Final colour for fragment is global ambient on material + I1 + I2 + I3
    gl_FragColor = (u_global_ambient * u_mat_ambient) + i_1 + i_2 + i_3;
}