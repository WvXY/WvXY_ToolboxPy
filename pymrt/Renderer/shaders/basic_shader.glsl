#version 460

#if defined VERTEX_SHADER

layout(location = 0) in vec2 vert;
layout(location = 1) in vec3 color;

uniform mat3 transform3 = mat3(1.0);

out vec3 fragColor;

void main() {
    fragColor = color;
    vec3 fixedPos = vec3(transform3 * vec3(vert, 1.0));
    gl_Position = vec4(fixedPos.xy, 0.0, 1.0);
}

#elif defined FRAGMENT_SHADER

in vec3 fragColor;

out vec4 outColor;

void main() {
    outColor = vec4(fragColor, 1.0);
}

#endif