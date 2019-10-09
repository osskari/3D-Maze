attribute vec3 a_position; // Material position
attribute vec3 a_normal; // Material normal

uniform mat4 u_model_matrix; // Model matrix
uniform mat4 u_view_matrix; // View matrix
uniform mat4 u_projection_matrix; // Projection matrix

uniform vec4 u_eye_position; // Position of eye

uniform vec4 u_light_position_1; // Position of light 1
uniform vec4 u_light_position_2; // Position of light 2
uniform vec4 u_light_position_3; // Position of light 3

varying vec4 v_normal; // Local coordinate varying normal

varying vec4 v_s_1; // S vector for light 1
varying vec4 v_h_1; // H vector for light 1

varying vec4 v_s_2; // S vector for light 2
varying vec4 v_h_2; // H vector for light 2

varying vec4 v_s_3; // S vector for light 3
varying vec4 v_h_3; // H vector for light 3

void main(void)
{
    // Material position converted to vec4 for matrix calculation
	vec4 position = vec4(a_position.x, a_position.y, a_position.z, 1.0);
    // Material normal converted to vec4 for matrix calcualtion
    vec4 normal = vec4(a_normal.x, a_normal.y, a_normal.z, 0.0);

	// local coordinates
    // Convert position to local coordinates
	position = u_model_matrix * position;
    // Convert normal to local coordinates
	v_normal = normalize(u_model_matrix * normal);

	// global coordinates
    // Convert position to global coordinates
	position = u_view_matrix * position;

	// S is the vector from material to light
	// V is the vector from material to eye
	// H is the halfway vector between eye and light
	// If H == material normal then eye and light are in mirrored positions over the material normal

    // Find V vector
	vec4 v = normalize(u_eye_position - position);

    // Find S vector for light 1
	v_s_1 = normalize(u_light_position_1 - position);
    // Find H vector for light 1
	v_h_1 = normalize(v_s_1+v);

    // Find S vector for light 2
	v_s_2 = normalize(u_light_position_2 - position);
    // Find H vector for light 2
	v_h_2 = normalize(v_s_2+v);

	// Find S vector for light 3
	v_s_3 = normalize(u_light_position_3 - position);
    // Find H vector for light 3
	v_h_3 = normalize(v_s_3+v);

    // Convert position to viewport coordinates
	position = u_projection_matrix * position;

    // Set position
	gl_Position = position;
}