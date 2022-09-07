from .Core import *

class WriterCSV(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Query", "SELECT * FROM input");

  def update(self):
    super().update()

    # write the file from input data 

    return 1;
