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
    // Array of S vector for each light
    vec4 s[3] = {v_s_1, v_s_2, v_s_3};
    // Array of H vector for each light
    vec4 h[3] = {v_h_1, v_h_2, v_h_3};
    // Array of ambient values for each light
    vec4 ambient[3] = {u_light_ambient_1, u_light_ambient_2, u_light_ambient_3};
    // Array of diffuse values for each light
    vec4 diffuse[3] = {u_light_diffuse_1, u_light_diffuse_2, u_light_diffuse_3};
    // Array of specular values for each light
    vec4 specular[3] = {u_light_specular_1, u_light_specular_2, u_light_specular_3};
    // Array to store lambert for each light
    float lambert[3];
    // Array to store Phong for each light
    float phong[3];
    // Variable for storing the sum of I for each light
    vec4 i_sum = vec4(0, 0, 0, 1);
    // For each light
    for(int i = 0; i < 3; i++){
        // Calculate lambert
        lambert[i] = max(dot(v_normal, s[i]), 0);
        //Calculate phong
        phong[i] = max(dot(v_normal, h[i]), 0);

        // I = light_amb * mat_amb + light_diff * mat_amb * lambert + light_spec * mat_spec * phong
        i_sum += ambient[i] * u_mat_ambient
                    + lambert[i] * diffuse[i] * u_mat_diffuse
                    + pow(phong[i], u_mat_shininess) * specular[i] * u_mat_specular;
    }
    // Final colour for fragment is global ambient on material + I1 + I2 + I3
    gl_FragColor = (u_global_ambient * u_mat_ambient) + i_sum;
}