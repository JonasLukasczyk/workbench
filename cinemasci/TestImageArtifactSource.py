from .Core import *

import sys
from PIL import Image, ImageFont, ImageDraw

class TestImageArtifactSource(Filter):

    Im_resolution = [640, 480]
    Im_background = (0, 0, 0)
    Im_fontsize   = 18
    Text_color    = (255, 255, 255)
    Text_offset   = 24
    Margin_left   = 50 
    Margin_top    = 50
    Tab           = 100

    def __init__(self):
        super(TestImageArtifactSource, self).__init__()

        # input/output ports
        self.addInputPort("Parameters", "Dictionary", [])
        self.addOutputPort("Artifacts", "List", [])

        # pick up class defaults
        self.im_background = TestImageArtifactSource.Im_background
        self.im_fontsize   = TestImageArtifactSource.Im_fontsize
        self.im_resolution = TestImageArtifactSource.Im_resolution
        self.text_color    = TestImageArtifactSource.Text_color
        self.text_offset   = TestImageArtifactSource.Text_offset
        self.margin_left   = TestImageArtifactSource.Margin_left
        self.margin_top    = TestImageArtifactSource.Margin_top
        self.tab           = TestImageArtifactSource.Tab

        # non class defaults
        self.cur_image = 0
        self.font = self.__get_font(self.im_fontsize) 

    def update(self):
        super().update()

        kwargs = self.inputs["Parameters"].getValue()
    
        newimage = self.__generate_image(kwargs)
        images.append(newimage)

        self.outputs["Artifacts"].setValue(images)

        return 1;

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
                font = ImageFont.truetype(font_name, size)
                break
            except IOError:
                continue

        return font

    # make an image
    def __generate_image(self, **kwargs):
        img = Image.new('RGB', (self.resolution[0], self.resolution[1]), color = self.im_background)

        im_name = f'{self.cur_image:03}.jpg'
        ImageDraw.Draw(img).rectangle((0, 0, self.im_resolution[0], self.im_resolution[1]), fill=self.im_background)

        #
        # write the parameters into the image
        #
        cur_x = self.margin_left
        cur_y = self.margin_top 
        for key, value in kwargs.items():
            cur_x  = self.margin_left
            cur_y += self.text_offset 
            ImageDraw.Draw(img).text((cur_x, cur_y), f'file:{key}', font=self.font, fill=self.text_color)
            cur_x += tab 
            ImageDraw.Draw(img).text((cur_x, cur_y), f'{value}', font=self.font, fill=self.text_color)

        self.cur_image += 1
