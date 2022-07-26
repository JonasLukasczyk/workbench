from .Core import *

import PIL

class Algorithm(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Query", "SELECT * FROM input");
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    # Black Magic
    images = self.inputs.Images.get()
    result = []

    for image in images:
        outImage = image.copy()
        rgbImage = PIL.Image.fromarray( image.channel["RGBA"] )
        outImage.channel['RGBA'] = numpy.array(rgbImage.convert('LA'))
        result.append(outimage)

    self.outputs.Images.set(result)

    return 1;
