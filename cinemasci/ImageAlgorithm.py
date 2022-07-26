from .Core import *

import PIL
import numpy
import cv2 

class ImageAlgorithm(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Images", []);
    self.addOutputPort("Images", []);

