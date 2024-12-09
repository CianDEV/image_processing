#version 330 core

in vec2 vert;      // Vertex position
in vec2 texcoord;  // Texture coordinates
out vec2 uvs;      // Pass texture coordinates to the fragment shader

void main() {
    uvs = texcoord;                      // Pass texture coordinates
    gl_Position = vec4(vert, 0.0, 1.0);  // Set clip-space position
}