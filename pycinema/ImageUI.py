from .Core import *

import matplotlib.pyplot as plt

import math

class ImageUI(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("Images", [])
        self.addInputPort("Container", None)
        self.container = None

        self.nImages = -1

        plt.ioff()
        self.fig = plt.figure()
        self.fig.tight_layout()

    def update(self):
        super().update()

        container = self.inputs.Container.get()
        if self.container!=container:
            self.container = container
            with self.container:
                self.fig.show()

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
                im = axis.imshow(image.channel['RGBA'])
                self.plots.append( [axis,im] )

        for i,image in enumerate(images):
            self.plots[i][1].set_data(image.channel['RGBA'])

        self.fig.subplots_adjust(
            left=0,
            bottom=0,
            right=1,
            top=1,
            wspace=0.05,
            hspace=0.05
        )

        self.fig.canvas.draw()

        return 1
