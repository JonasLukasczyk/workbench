__all__ = ["smoke"]

from .Core import *
from .CinemaDatabaseReader import *
from .DatabaseQuery import *
from .ImageEstimator import *
from .ImageReader import *
from .ImageWriter import *
from .ImageRenderer import *
from .ArtifactSource import *
from .CinemaArtifactSource import *
from .TestImageArtifactSource import *
from .DemoCDB import *
from .ImageUI import *
from .ParameterWidgets import *
from .Annotation import *
from .ImageConvert import *
from .ImageCanny import *
from .ColorMapping import *
from .DepthCompositing import *
from .ShaderSSAO import *
from .ImageGeneratorCNN import *
from .Color import *
from .MaskCompositing import *
from .Viewer import *

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
