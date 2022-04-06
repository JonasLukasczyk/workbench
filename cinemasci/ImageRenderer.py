from .Core import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GL import shaders
from OpenGL.GL import glGetString
import numpy as np

from PIL import Image

class ImageRenderer(Filter):
    def __init__(self):
        super(ImageRenderer, self).__init__();
        self.addInputPort("Image", "List", []);
        self.addOutputPort("Image", "List", []);

        # create context once
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)

    def compileShader(self, shader_code, shader_type):
        try:
            shader_id = glCreateShader(shader_type)
            glShaderSource(shader_id, shader_code)
            glCompileShader(shader_id)
            if glGetShaderiv(shader_id, GL_COMPILE_STATUS) != GL_TRUE:
                info = glGetShaderInfoLog(shader_id)
                raise RuntimeError('Shader compilation failed: %s' % (info))
            return shader_id
        except:
            glDeleteShader(shader_id)
            raise

    def getVertexShaderCode(self):
        return """
#version 120

attribute vec3 position;
varying vec2 vUV;

void main(){
    vUV = position.xy/2. + vec2(0.5);
    gl_Position = vec4(position,1);
}
        """

    def getFragmentShaderCode(self):
        return """
#version 120

uniform sampler2D tex;

varying vec2 vUV;

void main(){
    vec4 c = texture2D(tex,vUV);
    gl_FragColor = vec4(vec3(0.299*c.r + 0.587*c.g + 0.114*c.b),1);
    // fout_color = c;
    // fout_color = vec4(vUV.yx,0,1);
    // fout_color = vec4(1,0,1,1);
}
        """

    def render(self,image):

        width = image.shape[1]
        height = image.shape[0]

        # Setup framebuffer
        framebuffer = glGenFramebuffers (1)
        glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)

        # Setup colorbuffer
        colorbuffer = glGenRenderbuffers (1)
        glBindRenderbuffer(GL_RENDERBUFFER, colorbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, colorbuffer)

        # Setup depthbuffer
        depthbuffer = glGenRenderbuffers (1)
        glBindRenderbuffer(GL_RENDERBUFFER,depthbuffer)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthbuffer)

        # check status
        status = glCheckFramebufferStatus(GL_FRAMEBUFFER)
        if status != GL_FRAMEBUFFER_COMPLETE:
            print( "!!! Error in framebuffer activation")
            return

        # initialize view port
        glViewport(0, 0, width, height)
        glClearColor(0, 1, 0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        # create texture
        textID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, textID)

        img_data = np.array(image, np.int8)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
        glEnable(GL_TEXTURE_2D)

        # create shader
        self.shader = glCreateProgram()
        vs_id = self.compileShader(self.getVertexShaderCode(), GL_VERTEX_SHADER)
        frag_id = self.compileShader(self.getFragmentShaderCode(), GL_FRAGMENT_SHADER)
        glAttachShader(self.shader, vs_id)
        glAttachShader(self.shader, frag_id)
        glLinkProgram(self.shader)
        glUseProgram(self.shader)

        # draw fullscreen quad
        glBegin(GL_QUADS) # Begin the sketch
        glVertex2f(-1, -1) # Coordinates for the bottom left point
        glVertex2f(1, -1) # Coordinates for the bottom right point
        glVertex2f(1, 1) # Coordinates for the top right point
        glVertex2f(-1, 1) # Coordinates for the top left point
        glEnd() # Mark the end of drawing

        glFlush()

        # read pixel data
        glReadBuffer(GL_COLOR_ATTACHMENT0)
        glPixelStorei(GL_PACK_ALIGNMENT, 1)
        data = glReadPixels (0, 0, width, height, GL_RGB,  GL_UNSIGNED_BYTE)
        image = Image.new ("RGB", (width, height), (0, 0, 0))
        image.frombytes(data)

        # clean up
        glDeleteTextures([textID])
        glDeleteFramebuffers (1,[framebuffer])

        return image

    def computeOutputs(self):

        images = self.inputs["Image"].getValue();

        # create hidden window
        window = glutCreateWindow("")
        glutHideWindow()

        results = []
        for image in images:
            results.append( self.render(image) )

        # delete hidden window
        glutDestroyWindow(window)
        glutMainLoopEvent()
        glutMainLoopEvent()

        self.outputs["Image"].setValue( results );

        return super(ImageRenderer, self).computeOutputs();
