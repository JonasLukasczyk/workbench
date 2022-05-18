from .Core import *

from ipywidgets import interact, widgets
from IPython import display
import matplotlib.pyplot as plt

import math

class ImageUI(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("Images", "List", [])

        self.nImages = -1

        plt.ioff()
        self.fig = plt.figure()

    def update(self):
        super().update()

        images = self.inputs.Images.get()
        nImages = len(images)

        if self.nImages != nImages:
            self.nImages = nImages
            self.fig.clear()
            self.plots = []
            dim = math.ceil(math.sqrt(self.nImages))
            for i,image in enumerate(images):
                axis = self.fig.add_subplot(dim, dim, i+1)
                axis.set_axis_off()
                im = axis.imshow(image)
                self.plots.append( [axis,im] )

        for i,image in enumerate(images):
            self.plots[i][1].set_data(image)

        self.fig.canvas.draw()


        return 1
