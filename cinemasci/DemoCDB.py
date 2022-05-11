from .Core import *

import numpy as np
import moderngl
from PIL import Image

class DemoCDB(Filter):
    def __init__(self):
        super().__init__()
        self.addInputPort("Resolution", "vec2", (256,256))
        self.addInputPort("PhiSamples", "vec3", (0,360,360))
        self.addInputPort("ThetaSamples", "vec3", (20,20,1))
        self.addInputPort("Time", "float", 0)
        self.addOutputPort("Images", "List", [])

        # create context
        self.ctx = moderngl.create_standalone_context(require=330)

        # fullscreen quad
        self.quad = self.ctx.buffer(
            np.array([
                1.0,    1.0,
                -1.0,    1.0,
                -1.0, -1.0,
                 1.0, -1.0,
                 1.0,    1.0
            ]).astype('f4').tobytes()
        )

        # program
        self.program = self.ctx.program(
            vertex_shader=self.getVertexShaderCode(),
            fragment_shader=self.getFragmentShaderCode(),
            varyings=["uv"]
        )
        self.vao = self.ctx.simple_vertex_array(self.program, self.quad, 'position')

    def getVertexShaderCode(self):
        return """
#version 330

in vec2 position;
out vec2 uv;

void main(){
    uv = position;
    gl_Position = vec4(position,0,1);
}
"""

    def getFragmentShaderCode(self):
        return """
#version 330

in vec2 uv;
out vec3 fragColor;
uniform vec2 iResolution;
uniform float iTime;
uniform float iPhi;
uniform float iTheta;

const int MAX_MARCHING_STEPS = 255;
const float MIN_DIST = 0.1;
const float MAX_DIST = 40.0;
const float EPSILON = 0.001;

float planeSDF(vec3 p) {
    return abs(p.y);
}

float sphereSDF(vec3 p, float r) {
    return length(p) - r;
}

vec2 compare(vec2 hit, float d, float id){
  return hit.x<d ? hit : vec2(d,id);
}

vec2 sceneSDF(vec3 p) {
    vec2 hit = vec2(planeSDF(p),0);
    hit = compare(hit, sphereSDF(p-2.0*vec3(cos(iTime),0.25,sin(iTime)), 0.25), 1);
    hit = compare(hit, sphereSDF(p-vec3(0,1,0),1), 2);
    return hit;
}

vec3 march(vec3 ro, vec3 rd, float tmin, float tmax) {
    vec3 hit = vec3(0,-1,tmin);
    for (int i = 0; i < MAX_MARCHING_STEPS; i++) {
        hit.xy = sceneSDF(ro + hit.z * rd);
        if (hit.x < EPSILON) {
            return hit;
        }
        hit.z += hit.x;
        if (hit.z >= tmax) {
            return hit;
        }
    }
    return hit;
}

vec3 estimateNormal(vec3 p) {
    return normalize(vec3(
        sceneSDF(vec3(p.x + EPSILON, p.y, p.z)).x - sceneSDF(vec3(p.x - EPSILON, p.y, p.z)).x,
        sceneSDF(vec3(p.x, p.y + EPSILON, p.z)).x - sceneSDF(vec3(p.x, p.y - EPSILON, p.z)).x,
        sceneSDF(vec3(p.x, p.y, p.z    + EPSILON)).x - sceneSDF(vec3(p.x, p.y, p.z - EPSILON)).x
    ));
}

vec3 phongBRDF(vec3 lightDir, vec3 rayDir, vec3 normal, vec3 diff, vec3 spec, float shininess) {
  vec3 color = diff;
  vec3 reflectDir = reflect(-lightDir, normal);
  float specDot = max(dot(reflectDir, rayDir), 0.0);
  color += pow(specDot, shininess) * spec;
  return color;
}

float softshadow(vec3 ro, vec3 rd, float tmin, float tmax)
{
  float res = 1.0;
  vec3 hit = vec3(0,-1,tmin);
  for (int i = 0; i < 16; i++) {
      hit.xy = sceneSDF(ro + hit.z * rd);
      res = min( res, 8.0*hit.x/hit.z );
      hit.z += hit.x;
  }
  return clamp( res, 0.0, 1.0 );
}

void main() {
    vec2 fragCoord = (uv*0.5+0.5)*iResolution;
    vec3 focal = normalize(vec3(
        cos(iPhi)*sin(iTheta),
        cos(iTheta),
        sin(iPhi)*sin(iTheta)
    ));

    float aspect = iResolution.x/iResolution.y;
    vec3 rayDir = -normalize(focal);
    vec3 up = vec3(0,1,0);
    vec3 right = normalize(cross(rayDir,up));
    vec3 up2 = -normalize(cross(rayDir,right));

    float scale = 2.0;
    vec3 origin = 15.0*focal + aspect*right*uv.x*scale + up2*uv.y*scale;

    vec3 hit = march(origin, rayDir, MIN_DIST, MAX_DIST);

    if (hit.z > MAX_DIST - EPSILON) {
        fragColor = vec3(0);
        return;
    }

    // The closest point on the surface to the eyepoint along the view ray
    vec3 p = origin + hit.z * rayDir;
    vec3 lightDir = normalize(vec3(1,1,0));
    vec3 normal = estimateNormal(p);

    vec3 materialColor = hit.y > 1.5 ? vec3(0.8,0,0) : hit.y > 0.5 ? vec3(0,0.8,0) :  vec3(0.3 + 0.1*mod( floor(1.0*p.z) + floor(1.0*p.x), 2.0));

    vec3 radiance = vec3(0);
    float irradiance = max(dot(lightDir, normal), 0.0);
    vec3 brdf = phongBRDF(lightDir, rayDir, normal, materialColor, vec3(1), 1000.0);
    radiance += brdf * irradiance * vec3(1);
    radiance *= softshadow(p, lightDir, MIN_DIST, MAX_DIST);

    fragColor = pow(radiance, vec3(1.0 / 2.2) ); // gamma correction

    //fragColor = color*(hit.z-MIN_DIST)/(MAX_DIST-MIN_DIST);
    //fragColor = estimateNormal(p);
}
        """

    def render(self,phi,theta):

        res = self.inputs["Resolution"].getValue()
        time = self.inputs["Time"].getValue()

        # create framebuffer
        fbo = self.ctx.simple_framebuffer(res)
        fbo.use()
        fbo.clear(0.0, 0.0, 0.0, 1.0)

        # render
        self.program['iResolution'].value = res
        self.program['iTime'].value = time
        self.program['iPhi'].value = phi
        self.program['iTheta'].value = theta
        self.vao.render(moderngl.TRIANGLE_STRIP)

        # read pixels
        image = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)

        # release resources
        fbo.release()

        return image

    def update(self):
        super().update()

        phiSamples = self.inputs["PhiSamples"].getValue();
        thetaSamples = self.inputs["ThetaSamples"].getValue();

        results = []
        for theta in range(thetaSamples[0],thetaSamples[1]+[0,1][thetaSamples[0]==thetaSamples[1]],thetaSamples[2]):
            for phi in range(phiSamples[0],phiSamples[1]+[0,1][phiSamples[0]==phiSamples[1]],phiSamples[2]):
                results.append(
                    self.render(
                        phi/360.0*2.0*np.pi,
                        (90-theta)/180.0*np.pi,
                    )
                )

        # self.ctx.release()

        self.outputs["Images"].setValue(results);

        return 1;
