#version 460

#define MAX_SEEDS 128

#if defined VERTEX_SHADER

layout (location = 0) in vec2 in_vert;

uniform mat3 transform = mat3(1.0);
uniform bool fullScreen = false;

vec2 fullScreenVerts[4] = vec2[](
    vec2(-1.0, -1.0),
    vec2(-1.0, 1.0),
    vec2(1.0, -1.0),
    vec2(1.0, 1.0)
);

void main() {
    if (fullScreen) {
        gl_Position = vec4(fullScreenVerts[gl_VertexID], 0.0, 1.0);
        return;
    }

    gl_Position = vec4((transform * vec3(in_vert, 1.0)).xy, 0.0, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 f_color;

uniform vec3 seeds[MAX_SEEDS];  // TODO: use push constants & weights
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
        vec3 iseed = transform * vec3(seeds[i].xy, 1.0);
        float dist = distance(ipos, iseed.xy) - seeds[i].z;
        if (dist < min_dist) {
            min_dist = dist;
            closest_seed = i;
        }
    }

    vec3 color = rand3(vec2(closest_seed, 0.5));
    f_color = vec4(color, 1.0);
}

#endif
