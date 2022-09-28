from .Core import *
import PIL
import numpy

class Border(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("Width", 10)
        self.addInputPort("Color", 'AUTO')
        self.addInputPort("Images", [])
        self.addOutputPort("Images", [])

    def update(self):
        super().update()

        images = self.inputs.Images.get()

        results = []
        if len(images)<1:
          self.outputs.Images.set(results)
          return 1

        color = self.inputs.Color.get()
        if color=='AUTO':
            mean = images[0].channel['RGBA'].mean(axis=(0,1))
            if (mean[0]+mean[1]+mean[2])/3<128:
                color = (255,255,255)
            else:
                color = (0,0,0)

        for image in images:
            # copy the input image
            rgba = image.channel["RGBA"]
            rgbImage = PIL.Image.fromarray( rgba )

            I1 = PIL.ImageDraw.Draw(rgbImage)
            shape = ((0,0), (rgba.shape[1] - 1, rgba.shape[0] - 1))
            I1.rectangle( shape, outline=color, width = self.inputs.Width.get() )

            outImage = image.copy()
            outImage.channel['RGBA'] = numpy.array(rgbImage)
            results.append( outImage )

        self.outputs.Images.set(results)

        return 1
