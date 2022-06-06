from .Core import *

import PIL
import numpy

class ImageReader(Filter):

    def __init__(self):
        super(ImageReader, self).__init__()
        self.addInputPort("Table", [])
        self.addInputPort("FileColumn", "FILE")
        self.addOutputPort("Images", [])

    def update(self):
        super().update()

        table = self.inputs.Table.get()
        fileColumn = self.inputs.FileColumn.get()

        try:
            fileColumnIdx = list(map(str.lower,table[0])).index(fileColumn.lower())
        except ValueError as e:
            return print("Table does not contain '" + fileColumn + "' column!")

        images = [];
        for i in range(1, len(table)):
            row = table[i]
            path = row[fileColumnIdx]
            rawImage = PIL.Image.open(path)

            image = Image({ 'RGB': numpy.asarray(rawImage) })
            for j in range(0, len(row)):
                image.meta[table[0][j]] = row[j]

            images.append( image )

        self.outputs.Images.set(images)

        return 1;
