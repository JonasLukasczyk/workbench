from .Core import *

class ArtifactSource(Filter):

    def __init__(self):
        super(ArtifactSource, self).__init__()

        # input/output ports
        self.addInputPort("Parameters", "Dictionary", [])
        self.addOutputPort("Artifacts", "List", [])

    def update(self):
        super().update()

        kwargs = self.inputs.Parameters.get()

        artifacts = self.generate_artifacts(**kwargs)

        self.outputs.Artifacts.set(artifacts)

        return 1;

    # generate the artifacts
    def generate_artifacts(self, **kwargs):
        # must be overridden by subclasses
        return []
