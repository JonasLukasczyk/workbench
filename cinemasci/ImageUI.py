from .Core import *

from ipywidgets import interact, widgets
from IPython import display
import matplotlib.pyplot as plt

class ImageUI(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("Images", "List", [])

        self.fig = plt.figure()
        self.fig.set_size_inches(10,10)
        plt.close(self.fig)

        self.plots = []
        self.hdisplay = None
        self.nImages = -1

    def show(self):
        self.hdisplay = display.display('', display_id=True)
        self.update()

    def update(self):
        super().update()

        images = self.inputs['Images'].getValue()
        nImages = len(images)

        if self.nImages != nImages:
            self.nImages = nImages
            self.fig.clear()
            self.plots = []
            for i in range(0,nImages):
                self.plots.append( self.fig.add_subplot(1, self.nImages, i+1) )

        for i in range(0,self.nImages):
            self.plots[i].imshow(images[i])

        if self.hdisplay != None:
            self.hdisplay.update(self.fig)


        return 1
