from .Core import *
from matplotlib import pyplot

class Display(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("Images", [])

    def update(self):
        super().update()

        # Display Results
        artifacts = self.inputs.Images.get();
        if len(artifacts) > 0:
            for i in range(len(artifacts)):
                artifact = artifacts[i]
                pyplot.imshow(artifact.channels['rgba'])
                pyplot.axis('off')
                pyplot.show()

        return 1
