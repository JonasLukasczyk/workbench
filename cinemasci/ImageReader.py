from .Core import *

import PIL
import numpy
import h5py
import os

class ImageReader(Filter):

    def __init__(self):
        super().__init__()
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

            filename, extension = os.path.splitext(path)
            extension = str.lower(extension[1:])

            image = None
            if extension == 'h5':
                image = Image()
                file = h5py.File(path, 'r')

                image.origin = numpy.array(file.get('origin'))
                for (g,v) in [('channel',image.channel), ('meta',image.meta)]:
                    group = file.get(g)
                    if group==None:
                        raise ValueError('h5 file not formatted correctly')
                    for k in group.keys():
                        v[k] = numpy.array(group.get(k))

                file.close()

            elif str.lower(extension) in ['png','jpg','jpeg']:
                rawImage = PIL.Image.open(path)
                if rawImage.mode == 'RGB':
                    rawImage = rawImage.convert('RGBA')

                image = Image({ 'RGBA': numpy.asarray(rawImage) })
                for j in range(0, len(row)):
                    image.meta[table[0][j]] = row[j]

            else:
                raise ValueError('Unable to read image: '+path)

            images.append( image )

        self.outputs.Images.set(images)

        return 1
