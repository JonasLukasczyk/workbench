from .Core import *

import numpy as np
import moderngl

class ShaderPhong(Filter):
    def __init__(self):
        super().__init__()
        self.addInputPort("Images", [])
        self.addInputPort("Ambient", 0.7)
        self.addInputPort("Diffuse", 0.7)
        self.addInputPort("Specular", 1.0)
        self.addInputPort("Exponent", 16.0)
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
        self.program['rgbaTex'] = 0
        self.program['depthTex'] = 1

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

in vec2 uv;
out vec4 outcolor;

uniform sampler2D rgbaTex;
uniform sampler2D depthTex;

uniform vec2 uResolution;

uniform float uAmbient;
uniform float uDiffuse;
uniform float uSpecular;
uniform float uExponent;

float readDepth( const in vec2 coord ){
  return texture( depthTex, coord ).r;
}

vec3 computeNormal(in vec2 uv, in float depth){
  vec2 pixelSize = 1./uResolution;
  vec3 eps = vec3( pixelSize.x, pixelSize.y, 0 );
  float depthN = readDepth(uv.xy + eps.zy);
  float depthS = readDepth(uv.xy - eps.zy);
  float depthE = readDepth(uv.xy + eps.xz);
  float depthW = readDepth(uv.xy - eps.xz);
  // vec3 dx = vec3(2.0*eps.xz,depthE-depthW);
  // vec3 dy = vec3(2.0*eps.zy,depthN-depthS);
  vec3 dx = vec3(eps.xz, abs(depth-depthW) < abs(depth-depthE)
    ? depthW-depth
    : depth-depthE
  );
  vec3 dy = vec3(eps.zy, abs(depth-depthN) < abs(depth-depthS)
    ? depth-depthN
    : depthS-depth
  );
  return normalize(cross(dx, dy));
}

vec4 compute(const in vec2 sampleUV, const in vec2 pixelUV){
    vec4 pixelAlbedoRGBA = texture2D( rgbaTex, pixelUV );
    vec4 sampleAlbedoRGBA = texture2D( rgbaTex, sampleUV );
    vec3 albedo = sampleAlbedoRGBA.rgb;
    float alpha = sampleAlbedoRGBA.a;
    float depth = readDepth(sampleUV);
    vec3 normal = computeNormal(sampleUV, depth);
    vec3 lightDir = normalize(vec3(1,1,1));
    vec3 viewDir = vec3(0,0,1);
    vec3 halfDir = normalize(lightDir + viewDir);
    float lambertian = max(dot(lightDir, normal), 0.0);
    float specAngle = max(dot(halfDir, normal), 0.0);
    float specular = lambertian > 0.0 ? pow(specAngle, uExponent) : 0.0;
    vec3 diffuseColor = albedo * lambertian;
    vec3 color = albedo*uAmbient + diffuseColor*uDiffuse + specular*uSpecular;
    return alpha<1.0 || depth==1.0
      ? vec4(pixelAlbedoRGBA.rgb,floor(alpha))
      : vec4(color,1.0)
    ;
}

void main(){
  vec2 pixelSize = 1.0/uResolution;
  vec2 eps = vec2(1,-1)*0.15;
  vec4 color = (
    compute(uv+eps.xx*pixelSize, uv)
    +compute(uv+eps.xy*pixelSize, uv)
    +compute(uv+eps.yy*pixelSize, uv)
    +compute(uv+eps.yx*pixelSize, uv)
  );
  outcolor = color/4.0;
}

"""

    def createTexture(self,location,res,components,dtype='f1'):
        tex = self.ctx.texture(res, components, dtype=dtype, alignment=1)
        tex.repeat_x = False
        tex.repeat_y = False
        tex.use(location=location)
        return tex

    def render(self,image):

        rgba = image.channel['RGBA']
        depth = image.channel['Depth']

        # create texture
        self.rgbaTex.write(rgba.tobytes())
        self.depthTex.write(depth.tobytes())

        # render
        self.fbo.clear(0.0, 0.0, 0.0, 1.0)
        self.vao.render(moderngl.TRIANGLE_STRIP)

        # read pixels
        rgbaBuffer = self.fbo.read(attachment=0,components=4)
        rgbaFlatArray = np.frombuffer(rgbaBuffer, dtype=np.uint8)
        rgbaArray = rgbaFlatArray.view()
        rgbaArray.shape = (self.fbo.size[1],self.fbo.size[0],4)

        outImage = image.copy()
        outImage.channel['RGBA'] = rgbaArray

        return outImage

    def update(self):
        super().update()

        results = []

        images = self.inputs.Images.get()
        if len(images)<1:
            self.outputs.Images.set(results)
            return 1

        # first image
        image0 = images[0]
        if not 'Depth' in image0.channel:
            self.outputs.Images.set(images)
            return 1

        shape = image0.channel['RGBA'].shape
        if len(shape)!=3:
            shape = (shape[0],shape[1],1)
        res = shape[:2][::-1]

        # set uniforms
        self.program['uResolution'].value = res
        self.program['uAmbient'].value = float(self.inputs.Ambient.get())
        self.program['uDiffuse'].value = float(self.inputs.Diffuse.get())
        self.program['uSpecular'].value = float(self.inputs.Specular.get())
        self.program['uExponent'].value = float(self.inputs.Exponent.get())

        # create framebuffer
        self.fbo = self.ctx.simple_framebuffer(res)
        self.fbo.use()

        # create textures
        self.rgbaTex = self.createTexture(0,res,shape[2],dtype='f1')
        self.depthTex = self.createTexture(1,res,1,dtype='f4')

        for image in images:
            results.append( self.render(image) )

        self.rgbaTex.release()
        self.depthTex.release()
        self.fbo.release()

        self.outputs.Images.set(results)

        return 1
