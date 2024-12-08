import sys  # System functions to shut down program properly
from array import array  # Faster than lists
import moderngl  # Used to apply shaders in Python
import pygame  # Graphics library

# Initialize pygame and create the display surface
screen = pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)  # Creates window for OpenGL
display = pygame.Surface((1280, 720))  # Will render everything onto a display, then added to the screen
clock = pygame.time.Clock()  # For setting framerate

# Load and scale the bike image to match the screen size
img = pygame.image.load('bike.png')
img = pygame.transform.scale(img, screen.get_size())


class Shaders:
    """Shader class for setting up and using shaders."""
    
    def __init__(self, surface):
        """Initialize OpenGL context, buffers, and shaders."""
        self.surface = surface
        self.ctx = moderngl.create_context()

        # Create a buffer for the quad vertices and texture coordinates
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,   # Top-left corner (position, texcoord)
            1.0, 1.0, 1.0, 0.0,    # Top-right corner
            -1.0, -1.0, 0.0, 1.0,  # Bottom-left corner
            1.0, -1.0, 1.0, 1.0    # Bottom-right corner
        ]))

        # Create the shader program with vertex and fragment shaders
        self.program = self.ctx.program(vertex_shader=self.vert_shader(), fragment_shader=self.frag_shader())
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

    def vert_shader(self) -> str:
        """Returns the vertex shader code as a string."""
        return '''
        #version 330 core

        in vec2 vert;      // Vertex position
        in vec2 texcoord;  // Texture coordinates
        out vec2 uvs;      // Pass texture coordinates to the fragment shader

        void main() {
            uvs = texcoord;                      // Pass texture coordinates
            gl_Position = vec4(vert, 0.0, 1.0);  // Set clip-space position
        }
        '''

    def frag_shader(self) -> str:
        """Returns the fragment shader code as a string."""
        return '''
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
        '''

    def surf_to_texture(self, surf):
        """Converts a pygame surface to an OpenGL texture."""
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def frame_texture(self):
        """Renders the frame and updates the texture."""
        frame_tex = self.surf_to_texture(self.surface)
        frame_tex.use(0)
        self.program['tex'] = 0
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        # Flip the display to show updated texture
        pygame.display.flip()
        frame_tex.release()


# Create an instance of the Shaders class
shader = Shaders(display)

# Main loop to keep the window open
while True:
    # Fill display with black background
    display.fill((0, 0, 0))

    # Render the bike image onto the display surface
    display.blit(img, (0, 0))

    # Event handling to close the window or exit the loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Call the shader to render and release the texture onto the display
    shader.frame_texture()

    # Blit the rendered content to the screen
    screen.blit(display, (0, 0))

    # Set the framerate to 30 FPS
    clock.tick(30)
