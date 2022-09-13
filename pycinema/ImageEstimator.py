from .Core import *
from .CinemaDatabaseReader import *
from .DatabaseQuery import *
from .ImageReader import *
from .ImageGeneratorCNN import *
from .Border import *

class ImageEstimator(Filter):

    def __init__(self):
        super(ImageEstimator, self).__init__()

        # input/output ports
        self.addInputPort("DBPath", "./")
        self.addInputPort("ModelPath", "./")
        self.addInputPort("Parameters", [])
        self.addOutputPort("Artifacts", [])

        # db path
        self.dbreader    = CinemaDatabaseReader();
        self.query       = DatabaseQuery();
        self.imageReader = ImageReader();

        # both
        self.border = Border();
        self.border.inputs.Width.set(1);

        # estimator path
        self.mlfilter = ImageGeneratorCNN();

    def update(self):
        super().update()

        # read the database
        self.dbreader.inputs.Path.set( self.inputs.DBPath.get() ); 
        # query for objects
        params = self.inputs.Parameters.get();
        self.query.inputs.Table.set(self.dbreader.outputs.Table);
        qstring = "SELECT * FROM INPUT WHERE phi = '{}' AND theta = '{}'".format(params[0], params[1])
        self.query.inputs.Query.set(qstring);

        # Read Data Products
        self.imageReader.inputs.Table.set(self.query.outputs.Table);

        #
        # get an image from the database, if that entry exists
        # otherwise, return an estimated image
        #
        if len(self.imageReader.outputs.Images.get()) > 0:
            # add a border
            self.border.inputs.Color.set("black");
            self.border.inputs.Images.set(self.imageReader.outputs.Images);

        else:
            # return an estimated image 
            self.mlfilter.inputs.Model.set(self.inputs.ModelPath.get(), False);
            self.mlfilter.inputs.Device.set('cpu',False);
            self.mlfilter.inputs.Params.set([params],False);
            self.mlfilter.inputs.VP.set(2,False);
            self.mlfilter.inputs.VPO.set(256,False);
            self.mlfilter.inputs.Channel.set(8,False);
            self.mlfilter.update();

            # add a border
            self.border.inputs.Color.set("red");
            self.border.inputs.Images.set(self.mlfilter.outputs.Images);


        self.outputs.Artifacts.set(self.border.outputs.Images);

        return 1;
