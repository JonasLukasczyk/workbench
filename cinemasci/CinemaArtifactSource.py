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
        return self.cdb.inputs.Path.get();

    @path.setter
    def path(self, value):
        self.cdb.inputs.Path.set( value );

    #
    # generate artifacts
    #
    def generate_artifacts(self, **kwargs):
        # do the query
        self.query.inputs.Table.set(self.cdb.outputs.Table);
        self.query.inputs.Query.set('SELECT * FROM input LIMIT 5 OFFSET 0');
        self.imageReader.inputs.Table.set(self.query.outputs.Table)
        # self.imageRenderer.inputs.Artifacts.set( self.imageReader.outputs.Images );

        return self.imageReader.outputs.Images
