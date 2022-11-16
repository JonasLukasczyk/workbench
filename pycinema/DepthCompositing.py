from .Core import *
import numpy

class DepthCompositing(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort('images_a', [])
        self.addInputPort('images_b', [])
        self.addInputPort('depth_channel', 'depth')
        self.addOutputPort('images', [])

    def compose(self,A,B,depthChannel):

        result = A.copy()

        mask = A.channels[depthChannel] > B.channels[depthChannel]

        for c in A.channels:
            data = numpy.copy(A.channels[c])
            data[mask] = B.channels[c][mask]
            result.channels[c] = data

        return result

    def update(self):
        super().update()

        imagesA = self.inputs.images_a.get()
        imagesB = self.inputs.images_b.get()

        results = []

        nImages = len(imagesA)
        if len(imagesB)>0 and nImages!=len(imagesB):
          print('ERROR', 'Input image lists must be of equal size.' )
          self.outputs.images.set(results)
          return 0

        depthChannel = self.inputs.depth_channel.get()

        if len(imagesA)==len(imagesB):
            for i in range(0,nImages):
                results.append(
                    self.compose(
                        imagesA[i],
                        imagesB[i],
                        depthChannel
                    )
                )
        elif len(imagesA)>0:
            result = imagesA[0]
            for i in range(1,nImages):
                result = self.compose(result,imagesA[i],depthChannel)
            results.append(result)

        self.outputs.images.set(results)

        return 1
