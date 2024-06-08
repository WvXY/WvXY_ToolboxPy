#version 460

#define MAX_SEEDS 16

#if defined VERTEX_SHADER

layout (location = 0) in vec2 in_vert;

void main() {
    gl_Position = vec4(in_vert, 0.0, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 f_color;

uniform vec2 seeds[MAX_SEEDS];
uniform int nSeeds;

uniform mat3 transform = mat3(1.0);
uniform vec2 resolution = vec2(800, 800);

//layout (push_constant) uniform Voronoi {
//vec2 seeds[MAX_SEEDS];
//int len;
//} voronoi;

// https://stackoverflow.com/questions/4200224/random-noise-functions-for-glsl
float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

vec3 rand3(vec2 co){
    return vec3(rand(co), rand(co + 1.0), rand(co - 1.0));
}

void main() {
    vec2 ipos = 2 * gl_FragCoord.xy / resolution - 1.0;
    float min_dist = 1.0e10;
    int closest_seed = 0;

    for (int i = 0; i < nSeeds; ++i) {
        vec3 iseed = transform * vec3(seeds[i], 1.0);
        float dist = distance(ipos, iseed.xy);
        if (dist < min_dist) {
            min_dist = dist;
            closest_seed = i;
        }
    }

    vec3 color = rand3(vec2(closest_seed, 0.5));
    f_color = vec4(color, 1.0);
}

#endif
