from .Core import *

import numpy as np
import moderngl

class ImageRenderer(Filter):
    def __init__(self):
        super().__init__()
        self.addInputPort("Images", [])
        self.addOutputPort("Images", [])

        # create context
        self.ctx = moderngl.create_standalone_context(require=330)
        # self.ctx.release()

        # fullscreen quad
        self.quad = self.ctx.buffer(
            np.array([
                 1.0,  1.0,
                -1.0,  1.0,
                -1.0, -1.0,
                 1.0, -1.0,
                 1.0,  1.0
            ]).astype('f4').tobytes()
        )

        # program
        self.program = self.ctx.program(
            vertex_shader=self.getVertexShaderCode(),
            fragment_shader=self.getFragmentShaderCode(),
            varyings=["uv"]
        )
        self.program['tex'] = 0

        self.vao = self.ctx.simple_vertex_array(self.program, self.quad, 'position')

    def getVertexShaderCode(self):
        return """
#version 330

in vec2 position;
out vec2 uv;

void main(){
    uv = position/2.0+0.5;
    gl_Position = vec4(position,0,1);
}
"""

    def getFragmentShaderCode(self):
        return """
#version 330

uniform sampler2D tex;

in vec2 uv;
out vec4 color;

void main(){
    vec4 c = texture(tex,uv);
    color = vec4(vec3(0.299*c.r + 0.587*c.g + 0.114*c.b),1.0);
}
"""

    def render(self,image):

        rgba = image.channels['rgba']

        # create texture
        texture = self.ctx.texture(rgba.shape[:2][::-1], rgba.shape[2], rgba.tobytes(), alignment=1)
        texture.use(location=0)

        # create framebuffer
        fbo = self.ctx.simple_framebuffer(rgba.shape[:2][::-1], components=4)
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)
        self.vao.render(moderngl.TRIANGLE_STRIP)

        # read pixels
        rgbBuffer = fbo.read(attachment=0,components=3)
        rgbFlatArray = np.frombuffer(rgbBuffer, dtype=np.uint8)
        rgbArray = rgbFlatArray.view()
        rgbArray.shape = (rgba.shape[0],rgba.shape[1],3)

        # release resources
        texture.release()
        fbo.release()

        outImage = image.copy()
        outImage.channels['rgba'] = rgbArray

        return outImage

    def update(self):
        super().update()

        images = self.inputs.Images.get()

        results = []
        for image in images:
            results.append( self.render(image) )

        self.outputs.Images.set(results)

        return 1
