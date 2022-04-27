from .Core import *

import numpy as np
import moderngl
from PIL import Image

class ImageRenderer(Filter):
  def __init__(self):
    super(ImageRenderer, self).__init__()
    self.addInputPort("Image", "List", [])
    self.addOutputPort("Image", "List", [])

    # create context
    self.ctx = moderngl.create_standalone_context()

    # fullscreen quad
    vertices = np.array([
      1.0,  1.0,
      -1.0,  1.0,
      -1.0, -1.0,
      -1.0, -1.0,
       1.0, -1.0,
       1.0,  1.0
    ])
    self.quad = self.ctx.buffer(vertices.astype('f4').tobytes())

    # program
    self.program = self.ctx.program(
      vertex_shader=self.getVertexShaderCode(),
      fragment_shader=self.getFragmentShaderCode(),
      varyings=["vUV"]
    )
    self.program['tex'] = 0

    self.vao = self.ctx.simple_vertex_array(self.program, self.quad, 'position')

  def getVertexShaderCode(self):
    return """
#version 330

attribute vec2 position;
varying vec2 vUV;

void main(){
  vUV = position/2. + vec2(0.5);
  vUV.y = -vUV.y;
  gl_Position = vec4(position,0,1);
}
    """

  def getFragmentShaderCode(self):
    return """
#version 330

uniform sampler2D tex;

varying vec2 vUV;

void main(){
  vec4 c = texture2D(tex,vUV);
  gl_FragColor = vec4(vec3(0.299*c.r + 0.587*c.g + 0.114*c.b),1);
  // gl_FragColor = c;
  // gl_FragColor = vec4(vUV.xy,0,1);
}
    """

  def render(self,image):

    # create texture
    texture = self.ctx.texture(image.shape[1::-1], image.shape[2], image)
    texture.use(location=0)

    # create framebuffer
    fbo = self.ctx.simple_framebuffer((image.shape[1], image.shape[0]))
    fbo.use()
    fbo.clear(0.0, 0.0, 0.0, 1.0)
    self.vao.render(moderngl.TRIANGLE_STRIP)

    # read pixels
    image = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)

    # release resources
    texture.release()
    fbo.release()

    return image

  def update(self):
    super().update()

    images = self.inputs["Image"].getValue();

    results = []
    for image in images:
      results.append( self.render(image) )

    self.outputs["Image"].setValue(results);

    return 1;
