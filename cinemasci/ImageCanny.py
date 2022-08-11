from .Core import *

import cv2

# ImageCanny filter
# Runs opencv canny edge detection filter, and creates an image of
# those edges, with transparancy everywhere but the edges
class ImageCanny(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Thresholds", [100, 150]);
    self.addInputPort("Images", []);
    self.addOutputPort("Images", []);

  def update(self):
    super().update()

    result = []
    # iterate over all the images in the input images
    for image in self.inputs.Images.get():
        # convert the input data into a form that cv uses
        cvimage = cv2.cvtColor(image.channel["RGBA"], cv2.COLOR_RGB2BGR)
        thresholds = self.inputs.Thresholds.get()

        # run the canny algorithm, using this object's thresholds
        # canny = cv2.Canny(cvimage, thresholds[0], thresholds[1])/255
        canny = cv2.Canny(cvimage, thresholds[0], thresholds[1])

        outImage = image.copy()
        outImage.channel['Canny'] = canny
        result.append(outImage)

    self.outputs.Images.set(result)

    return 1;
