from .Core import *
import numpy

class Color(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort('rgba', (0,0,0,255))
        self.addOutputPort('rgba', (0,0,0,255))

    def update(self):
        super().update()

        self.outputs.RGBA.set(
          self.inputs.RGBA.get()
        )

        return 1
