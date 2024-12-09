#version 330 core

uniform sampler2D tex;    // Base texture
in vec2 uvs;              // Texture coordinates passed from the vertex shader
out vec4 f_color;         // Final color output for the fragment

void main() {
    // Simply output the color from the texture without any modification
    f_color = texture(tex, uvs);
}