from .Core import *

import csv

class DatabaseReader(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Path", "String", "./");
    self.addInputPort("FileColumn", "String", "FILE");
    self.addOutputPort("Table", "Table", []);

  def update(self):
    super().update()

    table = [];
    dbPath = self.inputs["Path"].getValue();
    dataCsvPath = dbPath + '/data.csv';
    with open(dataCsvPath, 'r+') as csvfile:
      spamreader = csv.reader(csvfile, delimiter=',')
      for row in spamreader:
        table.append(row)

    # remove empty lines
    table = list(filter(lambda row: len(row)>0, table))

    # add dbPath prefix to file column
    fileColumnIdx = table[0].index( self.inputs["FileColumn"].getValue() );
    for i in range(1,len(table)):
      table[i][fileColumnIdx] = dbPath + '/' + table[i][fileColumnIdx];

    self.outputs["Table"].setValue(table);

    return 1;
