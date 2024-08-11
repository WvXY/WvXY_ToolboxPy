#version 460

#if defined VERTEX_SHADER

layout(location = 0) in vec4 vert;  // (x, y, texCoordX, texCoordY)
//layout(location = 1) in vec2 texCoord;
out vec2 fragTexCoord;

void main() {
    gl_Position = vec4(vert.xy, 0.0, 1.0);
    fragTexCoord = vert.zw;
}

#elif defined FRAGMENT_SHADER

in vec2 fragTexCoord;
out vec4 fragColor;

uniform sampler2D image;

void main() {
    fragColor = texture(image, fragTexCoord);
}

#endif