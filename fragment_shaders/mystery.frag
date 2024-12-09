#version 330 core

in vec2 uvs;                
out vec4 f_color;           

uniform sampler2D tex;      
uniform float time;         

void main() {
    vec4 texColor = texture(tex, uvs);

    float grayscale = dot(texColor.rgb, vec3(0.3, 0.59, 0.11)); // Luminance formula
    vec3 desaturatedColor = mix(vec3(grayscale), texColor.rgb, 0.4); // Blend with 40% original color

    vec3 ninjaColor = vec3(0.2, 0.2, 0.3) + desaturatedColor * 0.8; // Subtle blue tint

    float vignette = smoothstep(0.7, 0.3, length(uvs - 0.5));
    ninjaColor *= mix(vec3(0.4, 0.4, 0.5), vec3(1.0), vignette); // Edge darkening

    float lightGradient = smoothstep(0.1, 0.9, uvs.y);
    ninjaColor *= mix(vec3(0.6, 0.6, 0.7), vec3(1.0), lightGradient); // Gradient dimming

    float flicker = 0.05 * sin(time * 5.0) + 0.95; // Slight variation in brightness
    ninjaColor *= flicker;

    f_color = vec4(ninjaColor, texColor.a);
}