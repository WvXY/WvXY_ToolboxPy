#version 460

#define PI 3.1415926535897932384626433832795
#define TWO_PI 6.283185307179586476925286766559
#define HALF_PI 1.5707963267948966192313216916398
#define QUARTER_PI 0.78539816339744830961566084581988
#define INV_PI 0.31830988618379067153776752674503

// https://stackoverflow.com/questions/4200224/random-noise-functions-for-glsl
//float rand(vec2 co){
//    return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
//}
//
//vec3 rand3(vec2 co){
//    return vec3(rand(co), rand(co + 1.0), rand(co - 1.0));
//}

#if defined VERTEX_SHADER

layout (location = 0) in vec2 pos;
layout (location = 1) in vec3 color;
layout (location = 2) in float size;

//uniform float point_size = 1.0;
uniform mat3 transform3 = mat3(1.0);

out vec3 fragColor;

void main() {
//    frag_color = rand3(vec2(iVert, 0.0));
    fragColor = color;
    vec3 fixedPos = transform3 * vec3(pos, 1.0);
    gl_Position = vec4(fixedPos.xy, 0.0, 1.0);
    gl_PointSize = size;
}

#elif defined FRAGMENT_SHADER

in vec3 fragColor;

out vec4 outColor;

uniform bool rectMode = false;

void main() {
    //    float dist = smoothstep(0.0, 0.5,
    //        distance(gl_PointCoord.xy, vec2(0.5)));
    //    out_color = vec4(frag_color, cos(dist * HALF_PI));
    // out_color = vec4(frag_color, 1.0 - dist * dist);
    if (!rectMode) {    // circle mode
        float dist = step(0.5, distance(gl_PointCoord.xy, vec2(0.5)));
        outColor = vec4(fragColor, 1.0 - dist);
        return;
    }
    outColor = vec4(fragColor, 1.0);
}

#endif