class Image():
    def __init__(self, channel={}, meta={}, origin=(0,0)):
        self.origin = origin
        self.channel = channel
        self.meta = meta

    def copy(self):
        return Image(
            self.channel.copy(),
            self.meta.copy(),
            self.origin
        )

    @property
    def shape(self):
        # get first channel
        for c in self.channel:
            return self.channel[c].shape

        return (0,0,0)

def isNumber(s):
    if type(s) == int or type(s) == float:
        return True
    if type(s) == str:
        return s.strip().lstrip('-').isnumeric()
    return False

class Port():
    def __init__(self, value, parent, isInput = False):
        self.parent = parent
        self._listeners = []
        if isInput:
            self._listeners.append(self.parent)
        self._value = value

    def get(self):
        if isinstance(self._value, Port):
            return self._value.get()
        return self._value;

    def set(self, value, update = True):
        # if old value is a port stop listing for push events
        if isinstance(self._value, Port):
            self._value._listeners.remove(self)

        # replace old value with new value
        self._value = value

        # if new value is a port listen for push events
        if isinstance(self._value, Port):
            self._value._listeners.append(self)

        # if value of a port was changed trigger update of listeners
        if update:
            for listener in self._listeners:
                if isinstance(listener, Port):
                    listener.parent.update()
                elif isinstance(listener, Filter):
                    listener.update()

class PortList():
    def __init__(self):
        return

class Filter():
    def __init__(self):
        self.inputs = PortList()
        self.outputs = PortList()

    def addInputPort(self, name, value):
        setattr(self.inputs, name, Port(value, self, True))

    def addOutputPort(self, name, value):
        setattr(self.outputs, name, Port(value, self))

    def update(self):
        # print("-> "+type(self).__name__)
        return
