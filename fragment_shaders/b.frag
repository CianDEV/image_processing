#version 330 core

uniform sampler2D tex;        // Base texture
uniform sampler2D glowMask;   // Glow mask texture
uniform float time;           // Time for animation (optional)

in vec2 uvs;                  // Texture coordinates from vertex shader
out vec4 f_color;             // Final fragment color output

void main() {
    // Fetch the base texture color
    vec4 baseColor = texture(tex, uvs);

    // Fetch the glow mask (defines glowing areas)
    vec4 glow = texture(glowMask, uvs);

    // Animate glow intensity using a sine wave
    float glowIntensity = 0.6 + 0.4 * sin(time * 2.0); // Subtle pulse

    // Define a mysterious glow color (cool tones)
    vec3 glowColor = vec3(0.3, 0.1, 0.5) * glow.rgb * glowIntensity;

    // Blend the glow with the base texture
    vec3 blendedColor = mix(baseColor.rgb, glowColor + baseColor.rgb, 0.5);

    // Darken the background slightly for contrast
    float darkenFactor = 0.85;
    vec3 finalColor = blendedColor * (1.0 - 0.2 * (1.0 - glow.a)) * darkenFactor;

    // Set the final output color
    f_color = vec4(finalColor, baseColor.a); // Preserve alpha
}