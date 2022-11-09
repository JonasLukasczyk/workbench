from .Core import *
from .Color import *
import numpy

class MaskCompositing(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort('ImagesA', [])
        self.addInputPort('ImagesB', [])
        self.addInputPort('Masks', [])
        self.addInputPort('ColorChannel', 'rgba')
        self.addInputPort('MaskChannel', 'mask')
        self.addInputPort('Opacity', 1.0)
        self.addOutputPort('Images', [])

    def update(self):
        super().update()

        imagesA = self.inputs.ImagesA.get()
        imagesB = self.inputs.ImagesB.get()
        masks = self.inputs.Masks.get()

        if not type(imagesA) is list:
          imagesA = [imagesA]
        if not type(imagesB) is list:
          imagesB = [imagesB]

        nImages = max(len(imagesA),len(imagesB))

        results = []

        colorChannel = self.inputs.ColorChannel.get()
        maskChannel = self.inputs.MaskChannel.get()

        for i in range(0,nImages):
            A = imagesA[min(i,len(imagesA)-1)]
            B = imagesB[min(i,len(imagesB)-1)]
            M = masks[min(i,len(masks)-1)]

            if type(A) is tuple and type(B) is tuple:
                print('ERROR', 'Unable to composit just two color inputs')
                return 0

            result = None

            Ac = None
            Bc = None
            Mc = M.channels[maskChannel]

            if type(A) is tuple:
                result = B.copy()
                Bc = B.channels[colorChannel]
                Ac = numpy.full(Bc.shape,A)
            elif type(B) is tuple:
                result = A.copy()
                Ac = A.channels[colorChannel]
                Bc = numpy.full(Ac.shape,B)
            else:
                result = A.copy()
                Ac = A.channels[colorChannel]
                Bc = B.channels[colorChannel]

            mask = Mc
            if numpy.isnan(mask).any():
              mask = numpy.nan_to_num(mask,nan=0,copy=True)

            if len(Ac.shape)>2 and Ac.shape[2]>1:
              mask = numpy.stack((mask,) * Ac.shape[2], axis=-1)

            if self.inputs.Opacity.get() != 1.0:
                mask = mask*self.inputs.Opacity.get()
            result.channels[colorChannel] = (1-mask)*Ac + mask*Bc
            if result.channels[colorChannel].dtype != Ac.dtype:
              result.channels[colorChannel] = result.channels[colorChannel].astype(Ac.dtype)

            results.append( result )

        self.outputs.Images.set(results)

        return 1
