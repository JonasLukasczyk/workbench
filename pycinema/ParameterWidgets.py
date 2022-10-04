from .Core import *

import ipywidgets

class ParameterWidgets(Filter):

    def __init__(self):
        super().__init__()
        self.addInputPort("Table", [])
        self.addInputPort("Container", None)
        self.addOutputPort("SQL", "SELECT * FROM input")
        self.widgets = []

    def generateWidgets(self):

        table = self.inputs.Table.get()
        header = table[0]
        self.widgets = []

        def on_change(change):
            if change['type'] == 'change' and change['name'] == 'value':
                self.update()

        for i in range(0,len(header)):
            if header[i].lower() == 'file' or header[i].lower() == 'id':
                continue

            vdic = set()

            for j in range(1,len(table)):
                vdic.add(table[j][i])

            o = list(vdic)
            isListOfNumbers = isNumber(table[1][i])
            if isListOfNumbers:
                o = [float(x) for x in o]
            o.sort()
            if isListOfNumbers:
                o = [str(x) for x in o]
            o.insert(0,'ANY')
            w = ipywidgets.SelectionSlider(
                options=o,
                value=o[1],
                description=header[i],
                callback_policy='mouseup'
            )

            w.observe(on_change)

            self.widgets.append(w)
        container = self.inputs.Container.get()
        if container!=None:
          container.children = self.widgets

    def update(self):
        super().update()

        table = self.inputs.Table.get()
        header = table[0]

        sql = 'SELECT * FROM input WHERE '

        # compute widgets
        if len(self.widgets) < 1:
            self.generateWidgets()

        for i in range(0,len(self.widgets)):
            if self.widgets[i].value == 'ANY':
                continue

            if self.widgets[i].value.isnumeric():
                sql = sql + '"' + self.widgets[i].description + '"=' + self.widgets[i].value + ' AND '
            else:
                sql = sql + '"' + self.widgets[i].description + '"="' + self.widgets[i].value + '" AND '

        if len(self.widgets) > 0:
            sql = sql[:-5]

        self.outputs.SQL.set(sql)

        return 1
