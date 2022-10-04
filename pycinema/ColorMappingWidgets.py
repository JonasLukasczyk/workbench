from .Core import *

import ipywidgets

class ColorMappingWidgets(Filter):

    def __init__(self):
        super().__init__()
        self.addInputPort("Images", [])
        self.addInputPort("Container", None)

        self.addOutputPort("Map", "plasma")
        self.addOutputPort("NaN", (0,0,0,0))
        self.addOutputPort("Range", (0,1))
        self.addOutputPort("Channel", "Depth")

        def on_change(change):
            if change['type'] == 'change' and change['name'] == 'value':
                self.update()
        def rgba_observer(change):
            if change['type'] == 'change' and change['name'] == 'value':
                disabled = change['new'] == 'RGBA'
                self.mapWidget.disabled = disabled
                self.minWidget.disabled = disabled
                self.maxWidget.disabled = disabled

        self.mapWidget = ipywidgets.Dropdown(
            description='Colormap:',
            options=[
                'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
                'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
                'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
                'plasma'
            ]
        )
        self.mapWidget.observe(on_change)

        self.minWidget = ipywidgets.FloatText(
            value=0,
            step=0.05,
            description='Min:'
        )
        self.minWidget.observe(on_change)
        self.maxWidget = ipywidgets.FloatText(
            value=1,
            step=0.05,
            description='Max:'
        )
        self.maxWidget.observe(on_change)

        self.channelWidget = ipywidgets.Dropdown(
            description='Channel:'
        )
        self.channelWidget.observe(on_change)
        self.channelWidget.observe(rgba_observer)

    def update(self):
        super().update()

        images = self.inputs.Images.get()

        # update channels if necessary
        if len(images):
            firstImage = images[0]
            if len(self.channelWidget.options)<1:
                channels = list(firstImage.channel.keys())
                channels.sort()
                self.channelWidget.options = channels
                if 'RGBA' in channels:
                    self.channelWidget.value = 'RGBA'

        # add widgets to container
        container = self.inputs.Container.get()
        if container!=None and len(container.children)==0:
            container.children = [
              self.channelWidget,
              self.mapWidget,
              self.minWidget,
              self.maxWidget
            ]

        # sync outputs with widgets
        if self.outputs.Map.get() != self.mapWidget.value:
            self.outputs.Map.set(self.mapWidget.value)
        if self.outputs.Channel.get() != self.channelWidget.value:
            self.outputs.Channel.set(self.channelWidget.value)
        range = self.outputs.Range.get()
        if range[0] != self.minWidget.value or range[1] != self.maxWidget.value:
            self.outputs.Range.set((self.minWidget.value,self.maxWidget.value))

        return 1
