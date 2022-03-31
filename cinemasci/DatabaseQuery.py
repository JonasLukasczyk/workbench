from .Core import *

import sqlite3

class DatabaseQuery(Filter):

    def __init__(self):
        super(DatabaseQuery, self).__init__();
        self.addInputPort("Table", "Table", []);
        self.addInputPort("Query", "String", "SELECT * FROM input");
        self.addOutputPort("Table", "Table", []);

    def executeSQL(self,db,sql):
#         print(sql)
        try:
            c = db.cursor()
            c.execute(sql)
        except sqlite3.Error as e:
            print(e)

    def createTable(self, db, table):
        sql = 'CREATE TABLE input(id INTEGER PRIMARY KEY AUTOINCREMENT';

        header = table[0]
        firstRow = table[1]

        for i in range(0,len(header)):
            sql = sql + ', ' + header[i];
            if firstRow[i].isnumeric():
                sql = sql + ' INTEGER';
            else:
                sql = sql + ' TEXT';

        sql =  sql + ')';
        self.executeSQL(db,sql)

    def insertData(self, db, table):
        sql = 'INSERT INTO input(';
        for x in table[0]:
            sql = sql + x + ', ';
        sql = sql[0:-2] + ') VALUES\n';

        for i in range(1, len(table)):
            row = '('
            for v in table[i]:
                row += '"' + v + '",'

            sql += row[0:-1] + '),\n'
        sql = sql[0:-2];
        self.executeSQL(db,sql)

    def queryData(self, db, sqlQuery):
        c = db.cursor();
        c.execute(sqlQuery);
        res = c.fetchall();
        columns = [];
        for d in c.description:
            columns.append(d[0]);
        res.insert(0,columns);
        return res;

    def computeOutputs(self):
        db = sqlite3.connect(":memory:");

        table = self.inputs["Table"].getValue();

        self.createTable(db, table);
        self.insertData(db, table);

        output = self.queryData(db, self.inputs["Query"].getValue());

        self.outputs["Table"].setValue(output);

        return super(DatabaseQuery, self).computeOutputs();
