from .Core import *

import cv2 

class ImageCanny(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Conversion", ImageConvertType.GREYSCALE);
    self.addInputPort("Thresholds", [100, 150]); 
    self.addInputPort("Conversion", ImageConvertType.GREYSCALE);
    self.addInputPort("Images", []);
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    result = []

    # iterate over all the images in the input images
    for image in self.inputs.Images.get(): 
        cvimage = cv2.cvtColor(image.channel["RGBA"], cv2.COLOR_RGB2BGR)
        thresholds = self.inputs.Thresholds.get()
        canny   = cv2.Canny(cvimage, thresholds[0], thresholds[1]) 
        cvFinal = cv2.cvtColor(canny, cv2.COLOR_BGR2RGB)
        outImage = image.copy()
        outImage.channel['RGBA'] = cvFinal 
        result.append(outImage)

    self.outputs.Images.set(result)

    return 1;
