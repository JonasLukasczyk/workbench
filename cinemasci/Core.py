class Port:
    def __init__(self, type, value, producer=''):
        self._type = type;
        self._value = value;
        self._producer = producer;

    def setValue(self,value):
        self._value = value;

    def getValue(self):
        if isinstance(self._value, Port):
            return self._value.getValue();

        if isinstance(self._producer, Filter):
            self._producer.computeOutputs();

        return self._value;

class Filter:
    def __init__(self):
        self.inputs = {}
        self.outputs = {}

    def addInputPort(self, name, type, value):
        self.inputs[name] = Port(type, value)

    def addOutputPort(self, name, type, value):
        self.outputs[name] = Port(type, value, self)

    def computeOutputs(self):
        print("-> "+type(self).__name__);
        return 1;
