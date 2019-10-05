attribute vec3 a_position;
attribute vec3 a_normal;

uniform mat4 u_model_matrix;
uniform mat4 u_view_matrix;
uniform mat4 u_projection_matrix;

uniform vec4 u_eye_position;

uniform vec4 u_light_position_1;
uniform vec4 u_light_position_2;

varying vec4 v_normal_1;
varying vec4 v_s_1;
varying vec4 v_h_1;

varying vec4 v_normal_2;
varying vec4 v_s_2;
varying vec4 v_h_2;

void main(void)
{
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
	vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// local coordinates
	position = u_model_matrix * position;
	v_normal_1 = normalize(u_model_matrix * normal);
	v_normal_2 = normalize(u_model_matrix * normal);

	// global coordinates
	v_s_1 = normalize(u_light_position_1 - position);
	vec4 v_1 = normalize(u_eye_position - position);
	v_h_1 = normalize(v_s_1+v_1);

	v_s_2 = normalize(u_light_position_2 - position);
	vec4 v_2 = normalize(u_eye_position - position);
	v_h_2 = normalize(v_s_2+v_2);

	position = u_view_matrix * position;
	position = u_projection_matrix * position;

	gl_Position = position;
}