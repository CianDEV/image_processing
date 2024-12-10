import sys  # System functions to shut down program properly
from array import array  # Faster than lists
import moderngl  # Used to apply shaders in Python
import pygame  # Graphics library
import os # OS functions for directory iteration

RES = (1548, 1000)

# Initialize pygame and create the display surface
screen = pygame.display.set_mode(RES, pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE)  # Creates window for OpenGL
display = pygame.Surface(RES)  # Will render everything onto a display, then added to the screen
clock = pygame.time.Clock()  # For setting framerate

# Load and scale the bike image to match the screen size
img = pygame.image.load('pictures/bike.jpg')
img = pygame.transform.smoothscale(img, RES)

# Load and set window icon
def window_config(icon, caption=''):
    icon = pygame.image.load(icon)
    pygame.transform.scale(icon, (32, 32))
    pygame.display.set_icon(icon)
    pygame.display.set_caption(caption)

window_config('icon.png', 'Image Processer')

class Shaders:
    """Shader class for setting up and using shaders."""
    
    def __init__(self, surface):
        """Initialize OpenGL context, buffers, and shaders."""
        # Set passed in surface attr as local variable
        self.surface = surface
        # Create OpenGl Context
        self.ctx = moderngl.create_context()

        # Create a buffer for the quad vertices and texture coordinates
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            -1.0, 1.0, 0.0, 0.0,   # Top-left corner (position, texcoord)
            1.0, 1.0, 1.0, 0.0,    # Top-right corner
            -1.0, -1.0, 0.0, 1.0,  # Bottom-left corner
            1.0, -1.0, 1.0, 1.0    # Bottom-right corner
        ]))
        
        # Fragment and vertex file dictionaries for storing filenames and corresponding content
        self.fragfile_contents = {}
        self.vertfile_contents = {}
        
        # Fragment and vertex file directories
        self.fragment_directory = 'fragment_shaders/'
        self.vertex_directory ='vertex_shaders/'
        
        # Read the files from fragment and vertex shader directories and store in the corresponding dictionaries
        self.fragment_shaders()
        self.vertex_shaders()
        
        # Create lists from the frag and vertex dictionary keys so they can be indexed numerically
        self.frag_keys = list(self.fragfile_contents.keys())
        self.vert_keys = list(self.vertfile_contents.keys())
        self.currentfragfile = 0
        self.currentvertfile = 0
        
        # Create the initial shader program with vertex and fragment shaders
        self.update_shader()
        
    def fragment_shaders(self):
        # Loop through each file in the directory
        for filename in os.listdir(self.fragment_directory):
            file_path = os.path.join(self.fragment_directory, filename)
            
            # Check if it's a file
            if os.path.isfile(file_path):
                # Open and read the file's content
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Store the filename and content in the fragfile_contents dictionary
                    self.fragfile_contents[filename] = content
  
    
    def vertex_shaders(self):
        # Loop through each file in the directory
        for filename in os.listdir(self.vertex_directory):
            file_path = os.path.join(self.vertex_directory, filename)
            
            # Check if it's a file
            if os.path.isfile(file_path):
                # Open and read the file's content
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Store the filename and content in the vertfile_contents dictionary
                    self.vertfile_contents[filename] = content
                    
    def update_shader(self):
        """Recompile and update the shader program with the current fragment shader."""
        # Update the shader program with the updated fragment and/or vertex shader
        self.program = self.ctx.program(
            vertex_shader=self.vertfile_contents[self.vert_keys[self.currentvertfile]],
            fragment_shader=self.fragfile_contents[self.frag_keys[self.currentfragfile]]
        )
        
        # Update the render object (VAO) to bind the updated program
        self.render_object = self.ctx.vertex_array(
            self.program, 
            [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')]
        )

    def surf_to_texture(self, surf):
        """Converts a pygame surface to an OpenGL texture."""
        # Create a texture with the surf size and allow 4 components (BGRA)
        tex = self.ctx.texture(surf.get_size(), 4)
        # Set the texture filtering to NEAREST for both minification and magnification.
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        # Set color channels to interpret as BGRA instead of RGBA 
        tex.swizzle = 'BGRA'
        # Write the data from the surface to the texture.
        tex.write(surf.get_view('1'))
        return tex

    def frame_texture(self):
        """Renders the frame and updates the texture."""
        # Convert surface into a texture
        frame_tex = self.surf_to_texture(self.surface)
        # Bind to texture unit 0, makes active texture
        frame_tex.use(0)
        # Assign tex unit 0 to tex uniform, links texture to shader
        self.program['tex'] = 0
        # Render object using triangle strip mode, connects vertices in strips creating triangles for rendering
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)

        # Flip the display to show updated texture
        pygame.display.flip()
        # Release the texture
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
            
        # Handle keypresses to cycle through shaders
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                shader.currentfragfile += 1
                shader.currentfragfile %= len(shader.frag_keys)
                shader.update_shader()
            if event.key == pygame.K_a:
                shader.currentfragfile -= 1
                shader.currentfragfile %= len(shader.frag_keys)
                shader.update_shader()

    # Call the shader to render and release the texture onto the display
    shader.frame_texture()

    # Blit the rendered content to the screen
    screen.blit(display, (0, 0))

    # Set the framerate to 30 FPS
    clock.tick(30)
    