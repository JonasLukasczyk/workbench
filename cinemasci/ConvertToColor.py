from .Core import *

import cv2 

class ConvertToColor(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Images", []);
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    result = []
    for image in self.inputs.Images.get(): 
        cvi = cv2.cvtColor(image.channel["RGBA"], cv2.COLOR_RGB2BGR)
        cvfinal = cv2.cvtColor(cvi, cv2.COLOR_BGR2RGB)
        outImage = image.copy()
        outImage.channel['RGBA'] = cvfinal
        result.append(outImage)

    self.outputs.Images.set(result)

    return 1;
