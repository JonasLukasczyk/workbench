from .Core import *
from .CinemaDatabaseReader import *
from .DatabaseQuery import *
from .ImageReader import *
from .ParameterWidgets import *
from .ColorMappingWidgets import *
from .ColorMapping import *
from .Annotation import *
from .ImageUI import *
from .ShaderSSAO import *

import IPython
import ipywidgets

class Viewer(Filter):

    def __init__(self, path, preload_query="SELECT * FROM input"):
        super().__init__()

        self.addInputPort("Path", "./")

        # accordion = widgets
        #   children=[],
        #   titles=('Parameters', 'Color Mapping'))
        # accordion

        self.parameterWidgetsContainer = ipywidgets.VBox();
        self.colorMappingWidgetsContainer = ipywidgets.VBox();

        self.leftColumn = ipywidgets.VBox([
          ipywidgets.Accordion(children=[self.parameterWidgetsContainer]),
          ipywidgets.Accordion(children=[self.colorMappingWidgetsContainer])
        ]);
        self.leftColumn.children[0].set_title(0,'Parameters')
        self.leftColumn.children[1].set_title(0,'Color Mapping')

        self.imageContainer = ipywidgets.Output()
        self.globalContainer = ipywidgets.HBox([self.leftColumn,self.imageContainer]);

        self.cinemaDatabaseReader  = CinemaDatabaseReader()
        self.cinemaDatabaseReader.inputs.Path.set(self.inputs.Path, False)

        preload_results = DatabaseQuery();
        preload_results.inputs.Table.set(self.cinemaDatabaseReader.outputs.Table, False);
        preload_results.inputs.Query.set(preload_query, False);

        self.parameterWidgets = ParameterWidgets()
        self.parameterWidgets.inputs.Table.set(preload_results.outputs.Table,False)
        self.parameterWidgets.inputs.Container.set(self.parameterWidgetsContainer,False)

        self.databaseQuery = DatabaseQuery()
        self.databaseQuery.inputs.Table.set(self.cinemaDatabaseReader.outputs.Table,False)
        self.databaseQuery.inputs.Query.set(self.parameterWidgets.outputs.SQL,False)

        self.imageReader = ImageReader()
        self.imageReader.inputs.Table.set(self.databaseQuery.outputs.Table,False)

        self.colorMappingWidgets = ColorMappingWidgets()
        self.colorMappingWidgets.inputs.Images.set(self.imageReader.outputs.Images,False)
        self.colorMappingWidgets.inputs.Container.set(self.colorMappingWidgetsContainer,False)

        self.colorMapping = ColorMapping()
        self.colorMapping.inputs.Images.set(self.imageReader.outputs.Images,False)
        self.colorMapping.inputs.Map.set(self.colorMappingWidgets.outputs.Map,False)
        self.colorMapping.inputs.Range.set(self.colorMappingWidgets.outputs.Range,False)
        self.colorMapping.inputs.Channel.set(self.colorMappingWidgets.outputs.Channel,False)

        self.shaderSSAO = ShaderSSAO()
        self.shaderSSAO.inputs.Images.set(self.colorMapping.outputs.Images,False)

        self.annotation = Annotation()
        self.annotation.inputs.Images.set(self.shaderSSAO.outputs.Images,False)

        self.imageUI = ImageUI()
        self.imageUI.inputs.Images.set( self.annotation.outputs.Images, False )
        self.imageUI.inputs.Container.set(self.imageContainer,False)

        IPython.display.display(self.globalContainer)

        self.inputs.Path.set(path)

    def update(self):
        super().update()
        return 1
