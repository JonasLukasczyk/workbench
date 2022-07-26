from .Core import *

import PIL
import numpy
import cv2 

class Algorithm(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Images", []);
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    # Black Magic
    result = []
    for image in self.inputs.Images.get(): 
        outImage = image.copy()
        # rgbImage = PIL.Image.fromarray( image.channel["RGBA"] )
        # outImage.channel['RGBA'] = numpy.array(rgbImage)
        cvi = cv2.cvtColor(image.channel["RGBA"], cv2.COLOR_RGB2GRAY)
        cvfinal = cv2.cvtColor(cvi, cv2.COLOR_BGR2RGB)
        outImage.channel['RGBA'] = cvfinal
        result.append(outImage)

    self.outputs.Images.set(result)

    return 1;
