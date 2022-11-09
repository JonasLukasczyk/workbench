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
        self.addInputPort("Cache", True)
        self.addOutputPort("Images", [])

        self.cache = {}

    def update(self):
        super().update()

        table = self.inputs.Table.get()
        fileColumn = self.inputs.FileColumn.get()

        try:
            fileColumnIdx = list(map(str.lower,table[0])).index(fileColumn.lower())
        except ValueError as e:
            print("Table does not contain '" + fileColumn + "' column!")
            return 0

        images = [];
        useCache = self.inputs.Cache.get()

        for i in range(1, len(table)):
            row = table[i]
            path = row[fileColumnIdx]

            filename, extension = os.path.splitext(path)
            extension = str.lower(extension[1:])

            image = None
            if useCache and path in self.cache:
                images.append(self.cache[path])
                continue

            if extension == 'h5':
                image = Image()
                file = h5py.File(path, 'r')
                for (g,v) in [('channels',image.channels), ('meta',image.meta)]:
                    group = file.get(g)
                    if group==None:
                        raise ValueError('h5 file not formatted correctly')
                    for k in group.keys():
                        v[k.lower()] = numpy.array(group.get(k))
                file.close()

            elif str.lower(extension) in ['png','jpg','jpeg']:
                rawImage = PIL.Image.open(path)
                if rawImage.mode == 'RGB':
                    rawImage = rawImage.convert('RGBA')
                image = Image({ 'rgba': numpy.asarray(rawImage) })

            else:
                raise ValueError('Unable to read image: '+path)

            # add meta data from data.csv
            for j in range(0, len(row)):
                key = table[0][j]
                if not key.lower() in image.meta:
                    image.meta[key.lower()] = row[j]

            if useCache:
                self.cache[path] = image

            images.append( image )

        self.outputs.Images.set(images)

        return 1
