from .Core import *

import cv2 

class ImageConvert(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Conversion", ImageConvertType.GREYSCALE);
    self.addInputPort("Images", []);
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    result = []
    for image in self.inputs.Images.get(): 

        if self.inputs.Conversion.get() == ImageConvertType.GREYSCALE:
            cvi = cv2.cvtColor(image.channel["RGBA"], cv2.COLOR_RGB2GRAY)
            cvfinal = cv2.cvtColor(cvi, cv2.COLOR_BGR2RGB)
            outImage = image.copy()
            outImage.channel['RGBA'] = cvfinal
            result.append(outImage)

        if self.inputs.Conversion.get() == ImageConvertType.COLOR:
            cvi = cv2.cvtColor(image.channel["RGBA"], cv2.COLOR_RGB2BGR)
            cvfinal = cv2.cvtColor(cvi, cv2.COLOR_BGR2RGB)
            outImage = image.copy()
            outImage.channel['RGBA'] = cvfinal
            result.append(outImage)

    self.outputs.Images.set(result)

    return 1;
