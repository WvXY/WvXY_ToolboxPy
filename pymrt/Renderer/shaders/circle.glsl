#version 460

#define PI 3.1415926535897932384626433832795
#define TWO_PI 6.283185307179586476925286766559
#define HALF_PI 1.5707963267948966192313216916398
#define QUARTER_PI 0.78539816339744830961566084581988
#define INV_PI 0.31830988618379067153776752674503

// https://stackoverflow.com/questions/4200224/random-noise-functions-for-glsl
float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

vec3 rand3(vec2 co){
    return vec3(rand(co), rand(co + 1.0), rand(co - 1.0));
}

#if defined VERTEX_SHADER

layout (location = 0) in vec2 vert;
layout (location = 1) in int vert_id;

uniform float point_size;

out vec3 frag_color;

void main() {
//    frag_color = vec3(
//        mod(vert_id * 432.43, 1.0),
//        mod(vert_id * 6654.32, 1.0),
//        mod(vert_id * 6544.11, 1.0)
//    );
    frag_color = rand3(vec2(vert_id, 0.5));
    gl_Position = vec4(vert.xy, 0.0, 1.0);
    gl_PointSize = point_size;
}

#elif defined FRAGMENT_SHADER

in vec3 frag_color;

out vec4 out_color;

void main() {
    float dist = smoothstep(0.0, 0.5,
        distance(gl_PointCoord.xy, vec2(0.5)));
    alpha = 1.0 - dist;
    out_color = vec4(frag_color, cos(dist * HALF_PI));
    // out_color = vec4(frag_color, 1.0 - dist * dist);

    // float dist = step(0.5, distance(gl_PointCoord.xy, vec2(0.5)));
    // out_color = vec4(frag_color,  1.0 - dist);
}

#endif