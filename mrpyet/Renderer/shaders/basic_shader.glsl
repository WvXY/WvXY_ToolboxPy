#version 460

#if defined VERTEX_SHADER

layout(location = 0) in vec2 vert;
layout(location = 1) in vec3 vert_color;

uniform mat3 transform = mat3(1.0);

out vec3 frag_color;

void main() {
    frag_color = vert_color;
    vec3 position = vec3(transform * vec3(vert, 1.0));
    gl_Position = vec4(position.xy, 0.0, 1.0);
}

#elif defined FRAGMENT_SHADER

in vec3 frag_color;

out vec4 out_color;

void main() {
    out_color = vec4(frag_color, 1.0);
}

#endif