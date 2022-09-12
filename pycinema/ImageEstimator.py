from .Core import *
from .CinemaDatabaseReader import *
from .DatabaseQuery import *
from .ImageReader import *
from .Annotation import *
from .ImageGeneratorCNN import *

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
        self.annotation  = Annotation();
        self.annotation.inputs.Color.set((255,0,0));
        self.annotation.inputs.Ignore.set(['FILE', 'id', 'phi', 'theta']);
        self.annotation.inputs.Size.set(6);
        self.annotation.inputs.XY.set((5,5));

        # estimator path
        self.mlfilter = ImageGeneratorCNN()

    def update(self):
        super().update()

        # read the database
        self.dbreader.inputs.Path.set( self.inputs.DBPath.get() ); 
        # query for objects
        params = self.inputs.Parameters.get();
        self.query.inputs.Table.set(self.dbreader.outputs.Table);
        qstring = "SELECT * FROM INPUT WHERE phi = '{}' AND theta = '{}' AND time = '{}'".format(params[0], params[1], params[2])
        self.query.inputs.Query.set(qstring);

        # Read Data Products
        self.imageReader.inputs.Table.set(self.query.outputs.Table);

        #
        # get an image from the database, if that entry exists
        # otherwise, return an estimated image
        #
        if len(self.imageReader.outputs.Images.get()) > 0:
            # add annotation
            self.annotation.inputs.Images.set(self.imageReader.outputs.Images);

        else:
            # return an estimated image 
            self.mlfilter.inputs.Model.set(self.inputs.ModelPath.get(), False);
            self.mlfilter.inputs.Device.set('cpu',False);
            self.mlfilter.inputs.Params.set([params],False);
            self.mlfilter.inputs.VP.set(3,False);
            self.mlfilter.inputs.VPO.set(256,False);
            self.mlfilter.inputs.Channel.set(8,False);
            self.mlfilter.update();

            # add annotation
            self.annotation.inputs.Images.set(self.mlfilter.outputs.Images);

        self.outputs.Artifacts.set(self.annotation.outputs.Images);

        return 1;
