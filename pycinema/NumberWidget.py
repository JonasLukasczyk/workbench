from .Core import *

import ipywidgets

class NumberWidget(Filter):

    def __init__(self,port,range=None):
        super().__init__()

        self.addOutputPort("Number", port.get())

        def on_change(change):
            if change['type'] == 'change' and change['name'] == 'value':
                if self.outputs.Number.get() != change['new']:
                    self.outputs.Number.set(change['new'])

        if range:
            self.widget = ipywidgets.FloatSlider(
                description=port.name,
                value=port.get(),
                min = range[0],
                max = range[1],
                step= range[2],
            )
        else:
            self.widget = ipywidgets.FloatText(
                description=port.name,
                value=port.get()
            )

        self.widget.observe(on_change)

        port.set(self.outputs.Number)

    def update(self):
        super().update()

        return 1
