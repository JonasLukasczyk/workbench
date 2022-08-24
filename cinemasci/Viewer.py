from .Core import *
from .CinemaDatabaseReader import *
from .DatabaseQuery import *
from .ImageReader import *
from .ParameterWidgets import *
from .Annotation import *
from .ImageUI import *

import IPython
import ipywidgets

class Viewer(Filter):

    def __init__(self, path):
        super().__init__()

        self.addInputPort("Path", "./")

        self.widgetContainer = ipywidgets.VBox();
        self.imageContainer = ipywidgets.Output()
        self.globalContainer = ipywidgets.HBox([self.widgetContainer,self.imageContainer]);

        self.cinemaDatabaseReader  = CinemaDatabaseReader()
        self.cinemaDatabaseReader.inputs.Path.set(self.inputs.Path, False)

        self.parameterWidgets = ParameterWidgets()
        self.parameterWidgets.inputs.Table.set(self.cinemaDatabaseReader.outputs.Table,False)
        self.parameterWidgets.inputs.Container.set(self.widgetContainer,False)

        self.databaseQuery = DatabaseQuery()
        self.databaseQuery.inputs.Table.set(self.cinemaDatabaseReader.outputs.Table,False)
        self.databaseQuery.inputs.Query.set(self.parameterWidgets.outputs.SQL,False)

        self.imageReader = ImageReader()
        self.imageReader.inputs.Table.set(self.databaseQuery.outputs.Table,False)

        self.annotation = Annotation()
        self.annotation.inputs.Images.set(self.imageReader.outputs.Images,False)

        self.imageUI = ImageUI()
        self.imageUI.inputs.Images.set( self.annotation.outputs.Images, False )
        self.imageUI.inputs.Container.set(self.imageContainer,False)

        IPython.display.display(self.globalContainer)

        self.inputs.Path.set(path)

    def update(self):
        super().update()
        return 1
