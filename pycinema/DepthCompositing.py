from .Core import *
import numpy

class DepthCompositing(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort('ImagesA', [])
        self.addInputPort('ImagesB', [])
        self.addInputPort('DepthChannel', 'Depth')
        self.addOutputPort('Images', [])

    def update(self):
        super().update()

        imagesA = self.inputs.ImagesA.get()
        imagesB = self.inputs.ImagesB.get()

        results = []

        nImages = len(imagesA)
        if nImages!=len(imagesB):
          print('ERROR', 'Input image lists must be of equal size.' )
          self.outputs.Images.set(results)
          return 0


        depthChannel = self.inputs.DepthChannel.get()

        for i in range(0,nImages):
            A = imagesA[i]
            B = imagesB[i]

            result = A.copy()

            mask = A.channel[depthChannel] > B.channel[depthChannel]

            for c in A.channel:
                data = numpy.copy(A.channel[c])
                data[mask] = B.channel[c][mask]
                result.channel[c] = data

            results.append( result )

        self.outputs.Images.set(results)

        return 1
