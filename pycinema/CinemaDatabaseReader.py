from .Core import *

import csv

class CinemaDatabaseReader(Filter):

  def __init__(self):
    super().__init__();
    self.addInputPort("Path", "./");
    self.addInputPort("FileColumn", "FILE");
    self.addOutputPort("Table", []);

  def update(self):
    super().update()

    table = [];
    dbPath = self.inputs.Path.get();
    dataCsvPath = dbPath + '/data.csv';
    with open(dataCsvPath, 'r+') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        for row in rows:
            table.append(row)

    # remove empty lines
    table = list(filter(lambda row: len(row)>0, table))

    # add dbPath prefix to file column
    fileColumnIdx = table[0].index( self.inputs.FileColumn.get() );
    for i in range(1,len(table)):
        table[i][fileColumnIdx] = dbPath + '/' + table[i][fileColumnIdx];

    self.outputs.Table.set(table);

    return 1;
