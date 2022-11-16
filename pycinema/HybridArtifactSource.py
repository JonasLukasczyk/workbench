from .Core import *
from .CinemaDatabaseReader import *
from .DatabaseQuery import *
from .ImageReader import *
from .ImageGeneratorCNN import *
from .Border import *

class HybridArtifactSource(Filter):

    def __init__(self):
        super(HybridArtifactSource, self).__init__()

        # input/output ports
        self.addInputPort("db_path", "./")
        self.addInputPort("force_database", False)
        self.addInputPort("force_estimator", False)
        self.addInputPort("model_path", "./")
        self.addInputPort("parameters", [])
        self.addOutputPort("artifacts", [])

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

        # depending upon state, load from different sources
        if self.inputs.force_database.get():
            self.loadFromDatabase()
        elif self.inputs.force_estimator.get():
            self.loadFromEstimator()
        else:
            numLoaded = self.loadFromDatabase();
            if numLoaded <= 0:
                self.loadFromEstimator();

        self.outputs.artifacts.set(self.border.outputs.images);

        return 1;

    def loadFromDatabase(self):
        # read the database
        self.dbreader.inputs.path.set( self.inputs.db_path.get() );

        # query for objects
        params = self.inputs.parameters.get();
        self.query.inputs.table.set(self.dbreader.outputs.table);
        qstring = "SELECT * FROM INPUT WHERE phi = '{}' AND theta = '{}'".format(params[0], params[1])
        self.query.inputs.query.set(qstring);

        # Read Data Products
        self.imageReader.inputs.table.set(self.query.outputs.table);

        # add a border
        self.border.inputs.color.set("black");
        self.border.inputs.images.set(self.imageReader.outputs.images);

        return len(self.imageReader.outputs.images.get());

    def loadFromEstimator(self):
        params = self.inputs.parameters.get();

        self.mlfilter.inputs.model.set(self.inputs.model_path.get(), False);
        self.mlfilter.inputs.device.set('cpu',False);
        self.mlfilter.inputs.params.set([params],False);
        self.mlfilter.inputs.vp.set(2,False);
        self.mlfilter.inputs.vpo.set(256,False);
        self.mlfilter.inputs.channel.set(8,False);
        self.mlfilter.update();

        # add a border
        self.border.inputs.color.set("red");
        self.border.inputs.images.set(self.mlfilter.outputs.images);

        return 1;
