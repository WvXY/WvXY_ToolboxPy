#version 460

#define MAX_SEEDS 128

// https://stackoverflow.com/questions/4200224/random-noise-functions-for-glsl
float rand(vec2 co){
    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
}

vec3 rand3(vec2 co){
    return vec3(rand(co), rand(co + 0.5), rand(co - 0.2));
}

#if defined VERTEX_SHADER

layout (location = 0) in vec2 vert;

uniform mat3 transform3 = mat3(1.0);
uniform bool fullCanvas = false;

vec2 fullCanvasVerts[4] = vec2[](
    vec2(-1.0, -1.0),
    vec2(-1.0, 1.0),
    vec2(1.0, 1.0),
    vec2(1.0, -1.0)
);

void main() {
    if (fullCanvas) {
        gl_Position = vec4(fullCanvasVerts[gl_VertexID], 0.0, 1.0);
        return;
    }

    gl_Position = vec4((transform3 * vec3(vert, 1.0)).xy, 0.0, 1.0);
}

#elif defined FRAGMENT_SHADER

out vec4 outColor;

uniform vec4 seeds[MAX_SEEDS];  // TODO: use push constants & weights
uniform int nSeeds;

uniform mat3 transform3 = mat3(1.0);
uniform mat3 transform3Inv = mat3(1.0);
uniform vec2 resolution = vec2(800, 800);

//layout (push_constant) uniform Voronoi {
//vec2 seeds[MAX_SEEDS];
//int len;
//} voronoi;

void main() {
    vec3 iPos = transform3Inv * vec3(2 * gl_FragCoord.xy / resolution - 1.0, 1.0);
    float minDist = 1.0e10;
    int iClosestSeed = 0;

    for (int i = 0; i < nSeeds; ++i) {
//        vec3 iSeed = transform3 * vec3(seeds[i].xy, 1.0);
        vec4 iSeed = seeds[i];
        float iDist = distance(vec3(iPos.xy, 0), iSeed.xyz) * iSeed.w;
        if (iDist < minDist) {
            minDist = iDist;
            iClosestSeed = i;
        }
    }

    vec3 color = rand3(vec2(iClosestSeed, 0.5));
    outColor = vec4(color, 1.0);
}

#endif
