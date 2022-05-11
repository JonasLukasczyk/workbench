class Port():
    def __init__(self, type, value, parent, isInput = False):
        self.type = type
        self.parent = parent
        self.isInput = isInput
        self._listeners = []
        self._value = value

    def getValue(self):
        if isinstance(self._value, Port):
            return self._value.getValue()
        return self._value;

    def setValue(self, value, update = True):
        # if old value is a port stop listing for push events
        if isinstance(self._value, Port):
            self._value._listeners.remove(self)

        # replace old value with new value
        self._value = value

        # if new value is a port listen for push events
        if isinstance(self._value, Port):
            self._value._listeners.append(self)

        # if value of an input port was changed trigger update of outputs
        if update and self.isInput:
            self.parent.update()

        # if value of an output port was changed trigger update of listeners
        if update and not self.isInput:
            for listener in self._listeners:
                listener.parent.update()

class Filter():
    def __init__(self):
        self.inputs = {}
        self.outputs = {}

    def addInputPort(self, name, type, value):
        self.inputs[name] = Port(type, value, self, True)

    def addOutputPort(self, name, type, value):
        self.outputs[name] = Port(type, value, self)

    def update(self):
        # print("-> "+type(self).__name__)
        return
