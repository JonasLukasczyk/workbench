from .Core import *
import numpy

class DepthCompositing(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("ImagesA", [])
        self.addInputPort("ImagesB", [])
        self.addOutputPort("Images", [])

    def update(self):
        super().update()

        imagesA = self.inputs.ImagesA.get()
        imagesB = self.inputs.ImagesB.get()

        nImages = len(imagesA)

        results = []

        for i in range(0,nImages):
            A = imagesA[i]
            B = imagesB[i]

            result = A.copy()

            mask = A.channel['Depth'] > B.channel['Depth']

            for c in A.channel:
                data = numpy.copy(A.channel[c])
                data[mask] = B.channel[c][mask]
                # print(data.shape)
                # print(B.channel[c].shape)
                # numpy.putmask(data,mask,B.channel[c])
                result.channel[c] = data

            results.append( result )

        self.outputs.Images.set(results)

        return 1
