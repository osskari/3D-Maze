uniform vec4 u_global_ambient;
uniform vec4 u_light_ambient_1;
uniform vec4 u_light_ambient_2;
uniform vec4 u_mat_ambient;

uniform vec4 u_light_diffuse_1;
uniform vec4 u_light_diffuse_2;
uniform vec4 u_mat_diffuse;

uniform vec4 u_light_specular_1;
uniform vec4 u_light_specular_2;
uniform vec4 u_mat_specular;

uniform float u_mat_shininess;

varying vec4 v_normal_1;
varying vec4 v_s_1;
varying vec4 v_h_1;

varying vec4 v_normal_2;
varying vec4 v_s_2;
varying vec4 v_h_2;

void main(void)
{
	float lambert_1 = max(dot(v_normal_1, v_s_1), 0);
	float phong_1 = max(dot(v_normal_1, v_h_1), 0);

    float lambert_2 = max(dot(v_normal_2, v_s_2), 0);
	float phong_2 = max(dot(v_normal_2, v_h_2), 0);

    vec4 i_1 = u_light_ambient_1 * u_mat_ambient
                   + lambert_1 * u_light_diffuse_1 * u_mat_diffuse
                   + u_light_specular_1 * u_mat_specular * pow(phong_1, u_mat_shininess);

    vec4 i_2 = u_light_ambient_2 * u_mat_ambient
                   + lambert_2 * u_light_diffuse_2 * u_mat_diffuse
                   + u_light_specular_2 * u_mat_specular * pow(phong_2, u_mat_shininess);

    gl_FragColor = (u_global_ambient * u_mat_ambient) + i_1 + i_2;
}