__all__ = ["smoke"]

from .Core import *

from .Annotation import *
from .Border import *
from .CinemaDatabaseReader import *
from .CinemaViewer import *
from .ColorMapping import *
from .ColorMappingWidgets import *
from .ColorSource import *
from .DatabaseQuery import *
from .DemoScene import *
from .DepthCompositing import *
from .HybridArtifactSource import *
from .ImageCanny import *
from .ImageConvert import *
from .ImageGeneratorCNN import *
from .ImageReader import *
from .ImageViewer import *
from .ImageWriter import *
from .MaskCompositing import *
from .NumberWidget import *
from .ParameterWidgets import *
from .Shader import *
from .ShaderPBR import *
from .ShaderPhong import *
from .ShaderSSAO import *

#
# new factory function
#
# creates new objects for a consistent high level interface
#
def new( vtype, args ):
    result = None
    if vtype == "cdb":
        if "path" in args:
            from . import cdb
            result = cdb.cdb(args["path"])
    else:
        print("ERROR: unsupported viewer type: {}".format(vtype))

    return result

def version():
    return "2.0"
