from .Core import *

from PIL import Image

class ImageReader(Filter):

  def __init__(self):
    super(ImageReader, self).__init__()
    self.addInputPort("Table", "Table", [])
    self.addInputPort("FileColumn", "String", "FILE")
    self.addOutputPort("Images", "List", [])

  def update(self):
    super().update()

    table = self.inputs["Table"].getValue()
    fileColumn = self.inputs["FileColumn"].getValue()

    try:
      fileColumnIdx = table[0].index(fileColumn)
    except ValueError as e:
      return print("Table does not contain '" + fileColumn + "' column!")

    images = [];
    for i in range(1, len(table)):
      path = table[i][fileColumnIdx]
      images.append( Image.open(path) )

    self.outputs["Images"].setValue(images)

    return 1;
