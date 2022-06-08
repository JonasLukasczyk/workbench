from .Core import *
import PIL
import numpy
import sys

class Annotation(Filter):

    def __init__(self):
        super().__init__()

        self.addInputPort("XY", (20,20))
        self.addInputPort("Size", 20)
        self.addInputPort("Spacing", 0)
        self.addInputPort("Color", (0,0,0))
        self.addInputPort("Images", [])
        self.addInputPort("Ignore", ['FILE'])
        self.addOutputPort("Images", [])

    #
    # solution from:
    # https://www.programcreek.com/python/?CodeExample=get+font
    #
    def __get_font(self, size):
        """Attempts to retrieve a reasonably-looking TTF font from the system.

        We don't make much of an effort, but it's what we can reasonably do without
        incorporating additional dependencies for this task.
        """
        if sys.platform == 'win32':
            font_names = ['Arial']
        elif sys.platform in ['linux', 'linux2']:
            font_names = ['DejaVuSans-Bold', 'DroidSans-Bold']
        elif sys.platform == 'darwin':
            font_names = ['Menlo', 'Helvetica']

        font = None
        for font_name in font_names:
            try:
                font = PIL.ImageFont.truetype(font_name, size)
                break
            except IOError:
                continue

        return font

    def update(self):
        super().update()

        images = self.inputs.Images.get()
        nImages = len(images)

        font = self.__get_font(self.inputs.Size.get())

        result = []
        ignoreList = list(map(str.lower, self.inputs.Ignore.get()))

        for image in images:
            rgbImage = PIL.Image.fromarray( image.channel["RGBA"] )
            text = ''
            for t in image.meta:
                if t.lower() in ignoreList:
                    continue
                text = text + ' ' + t+': '+str(image.meta[t]) + '\n'

            I1 = PIL.ImageDraw.Draw(rgbImage)
            I1.multiline_text(
                self.inputs.XY.get(),
                text,
                fill=self.inputs.Color.get(),
                font=font,
                spacing=self.inputs.Spacing.get()
            )

            outImage = image.copy()
            outImage.channel['RGBA'] = numpy.array(rgbImage)
            result.append( outImage )

        self.outputs.Images.set(result)

        return 1
