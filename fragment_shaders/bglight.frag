#version 330 core

uniform sampler2D tex;       // The texture to apply on the background
uniform vec3 lightColor;     // The color of the light
uniform vec3 lightDirection; // Direction of the light source (normalized)
uniform float time;          // Time for animation effect (optional)

in vec2 uvs;                 // Texture coordinates from the vertex shader
out vec4 f_color;            // Final color output for the fragment

void main() {
    // Fetch the base texture color from the background
    vec4 baseColor = texture(tex, uvs);

    // Calculate ambient light intensity (constant for all fragments)
    float ambientStrength = 0.2; // Low ambient light intensity
    vec3 ambientLight = ambientStrength * lightColor;

    // Calculate directional light intensity (affects light direction and angle)
    float diff = max(dot(lightDirection, normalize(vec3(0.0, 0.0, 1.0))), 0.0);
    vec3 diffuseLight = (1.0 - diff) * lightColor; // Light decreases as the angle gets steeper

    // Combine the ambient and directional lighting
    vec3 enhancedColor = (baseColor.rgb + ambientLight + diffuseLight);

    // Optionally animate the lighting over time (e.g., simulate a pulsing light effect)
    enhancedColor *= 0.5 + 0.5 * sin(time * 2.0); // Light pulses over time

    // Set the final output color
    f_color = vec4(enhancedColor, baseColor.a); // Preserve the texture's alpha
}
