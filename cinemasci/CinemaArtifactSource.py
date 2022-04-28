from .Core import *
from .ArtifactSource import *
from .DatabaseQuery import *
from .CinemaDatabaseReader import *
from .ImageReader import *
from .ImageRenderer import *

import sys

#
# A class that provides artifacts in a cinema-compliant way
#
class CinemaArtifactSource(ArtifactSource):

    def __init__(self):
        super(CinemaArtifactSource, self).__init__()

        # input/output ports
        self.addInputPort("Parameters", "Dictionary", [])
        self.addOutputPort("Artifacts", "List", [])

        # instance variables 
        self.cdb = CinemaDatabaseReader();
        self.query = DatabaseQuery();
        self.imageReader = ImageReader();
        # self.imageRenderer = ImageRenderer();

    #
    # get and set properties
    #
    @property
    def path(self):
        return self.cdb.inputs["Path"].getValue(); 

    @path.setter
    def path(self, value):
        self.cdb.inputs["Path"].setValue( value );

    #
    # generate artifacts 
    #
    def generate_artifacts(self, **kwargs):
        # do the query
        self.query.inputs["Table"].setValue(self.cdb.outputs['Table']);
        self.query.inputs["Query"].setValue('SELECT * FROM input LIMIT 5 OFFSET 0');
        self.imageReader.inputs["Table"].setValue(self.query.outputs['Table'])
        # self.imageRenderer.inputs["Artifacts"].setValue( self.imageReader.outputs["Images"] );

        return self.imageReader.outputs["Images"]
